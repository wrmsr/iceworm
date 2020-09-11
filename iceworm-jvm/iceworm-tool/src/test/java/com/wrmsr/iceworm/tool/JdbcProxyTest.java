package com.wrmsr.iceworm.tool;

import org.junit.Test;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.lang.reflect.Proxy;
import java.sql.*;
import java.util.*;
import java.util.concurrent.Callable;
import java.util.logging.Logger;

public class JdbcProxyTest
{
    public static class WrappingDriver implements Driver
    {
        public final static String URL_PREFIX = "iw:";

        @Override
        public Connection connect(String url, Properties info) throws SQLException
        {
            String unwrappedUrl = url.substring(URL_PREFIX.length());

            Driver underlyingDriver;
            try {
                underlyingDriver = DriverManager.getDriver(unwrappedUrl);
            } catch (SQLException e) {
                throw new SQLException();
            }

            Connection connection = wrapConnection(
                    unwrappedUrl,
                    info,
                    () -> underlyingDriver.connect(unwrappedUrl, info));
            return connection;
        }

        public Connection wrapConnection(
                String url,
                Properties info,
                Callable<Connection> underlyingConnectionCreator
        ) throws SQLException
        {
            Connection connection;
            try {
                connection = underlyingConnectionCreator.call();
            } catch (Exception e) {
                if (e.getCause() instanceof SQLException) {
                    throw (SQLException) e.getCause();
                } else {
                    throw new SQLException(e);
                }
            }

            if (connection == null) {
                return null;
            }

            if (Proxy.isProxyClass(connection.getClass()) &&
                    Proxy.getInvocationHandler(connection).getClass() == ConnectionInvocationHandler.class) {
                return connection;
            }

            Properties cleanedConnectionProperties = new Properties();
            if (info != null) {
                for (String str : info.stringPropertyNames()) {
                    if (!str.toLowerCase().contains("password")) {
                        cleanedConnectionProperties.setProperty(str, info.getProperty(str));
                    }
                }
            }

            ConnectionInvocationHandler connectionInvocationHandler = new ConnectionInvocationHandler(
                    connection,
                    url,
                    cleanedConnectionProperties);
            connection = (Connection) Proxy.newProxyInstance(connection.getClass().getClassLoader(),
                    extractAllInterfaces(connection.getClass()),
                    connectionInvocationHandler);

            return connection;
        }

        private static class ConnectionInvocationHandler implements InvocationHandler
        {
            private final Connection wrappedConnection;
            private final String url;
            private final Properties connectionProperties;

            public ConnectionInvocationHandler(Connection wrappedConnection, String url, Properties connectionProperties)
            {
                this.wrappedConnection = wrappedConnection;
                this.url = url;
                this.connectionProperties = connectionProperties;
            }

            @Override
            public Object invoke(Object proxy, Method method, Object[] args) throws Throwable
            {
                String methodName = method.getName();

                Object result = invokeUnwrapException(wrappedConnection, method, args);
                if (result != null) {
                    if ("createStatement".equals(methodName)) {
                        return Proxy.newProxyInstance(
                                result.getClass().getClassLoader(),
                                extractAllInterfaces(result.getClass()),
                                new StatementInvocationHandler((Statement) result));
                    } else if (("prepareStatement".equals(methodName) || "prepareCall".equals(methodName)) && args != null) {
                        return Proxy.newProxyInstance(
                                result.getClass().getClassLoader(),
                                extractAllInterfaces(result.getClass()),
                                new PreparedStatementInvocationHandler((PreparedStatement) result, (String) args[0]));
                    }
                }

                return result;
            }
        }

        private static class StatementInvocationHandler implements InvocationHandler
        {
            private final Statement wrappedStatement;

            public StatementInvocationHandler(Statement wrappedStatement)
            {
                this.wrappedStatement = wrappedStatement;
            }

            @Override
            public Object invoke(Object proxy, Method method, Object[] args) throws Throwable
            {
                if ("executeQuery".equals(method.getName())) {
                    if ("select 2".equals(args[0])) {
                        args[0] = "select 200";
                    }
                }

                Object result;
                result = invokeUnwrapException(wrappedStatement, method, args);
                return result;
            }
        }

        private static class PreparedStatementInvocationHandler implements InvocationHandler
        {
            private final PreparedStatement wrappedStatement;
            private final String sql;

            public PreparedStatementInvocationHandler(PreparedStatement wrappedStatement, String sql)
            {
                this.wrappedStatement = wrappedStatement;
                this.sql = sql;
            }

            @Override
            public Object invoke(Object proxy, Method method, Object[] args) throws Throwable
            {
                Object result;
                result = invokeUnwrapException(wrappedStatement, method, args);
                return result;
            }
        }

        private static Object invokeUnwrapException(
                Object target,
                Method method,
                Object[] args
        )
                throws Throwable
        {
            try {
                return method.invoke(target, args);
            } catch (final InvocationTargetException e) {
                throw e.getCause();
            }
        }


        private static Class<?>[] extractAllInterfaces(Class<?> clazz)
        {
            Set<Class<?>> interfaces = new HashSet<>();
            for (Class<?> currClazz = clazz; currClazz != null; currClazz = currClazz.getSuperclass()) {
                Collections.addAll(interfaces, currClazz.getInterfaces());
            }

            return interfaces.toArray(new Class[0]);
        }

        @Override
        public boolean acceptsURL(String url) throws SQLException
        {
            return url != null && url.startsWith(URL_PREFIX);
        }

        @Override
        public DriverPropertyInfo[] getPropertyInfo(String url, Properties info) throws SQLException
        {
            return new DriverPropertyInfo[0];
        }

        @Override
        public int getMajorVersion()
        {
            return 1;
        }

        @Override
        public int getMinorVersion()
        {
            return 0;
        }

        @Override
        public boolean jdbcCompliant()
        {
            return false;
        }

        @Override
        public Logger getParentLogger() throws SQLFeatureNotSupportedException
        {
            throw new SQLFeatureNotSupportedException();
        }
    }

    @Test
    public void testWrapper() throws Throwable
    {
        Driver driver = new WrappingDriver();
        try (Connection conn = driver.connect("iw:jdbc:h2:mem:db1", new Properties())) {
            Statement stmt = conn.createStatement();
            for (int i = 1; i < 4; ++i) {
                System.out.println(i);
                try (ResultSet rs = stmt.executeQuery(String.format("select %d", i))) {
                    while (rs.next()) {
                        System.out.println(rs.getInt(1));
                    }
                }
                System.out.println();
            }
        }
    }
}
