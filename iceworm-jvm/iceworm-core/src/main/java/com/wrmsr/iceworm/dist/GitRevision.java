package com.wrmsr.iceworm.dist;

import com.google.common.io.CharStreams;
import com.wrmsr.iceworm.util.lazy.SupplierLazyValue;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Optional;

public final class GitRevision
{
    private GitRevision()
    {
    }

    private static final SupplierLazyValue<Optional<String>> revision = new SupplierLazyValue<>();

    public static Optional<String> get()
    {
        return revision.get(() -> {
            InputStream stream = GitRevision.class.getResourceAsStream(".revision");
            if (stream != null) {
                try {
                    String rev = CharStreams.toString(new InputStreamReader(stream));
                    return Optional.of(rev.trim());
                }
                catch (IOException e) {
                    throw new RuntimeException(e);
                }
            }
            else {
                return Optional.empty();
            }
        });
    }
}
