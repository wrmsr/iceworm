/*eslint-disable block-scoped-var, id-length, no-control-regex, no-magic-numbers, no-prototype-builtins, no-redeclare, no-shadow, no-var, sort-vars*/
"use strict";

var $protobuf = require("protobufjs/minimal");

// Common aliases
var $Reader = $protobuf.Reader, $Writer = $protobuf.Writer, $util = $protobuf.util;

// Exported root namespace
var $root = $protobuf.roots["default"] || ($protobuf.roots["default"] = {});

$root.iceworm = (function() {

    /**
     * Namespace iceworm.
     * @exports iceworm
     * @namespace
     */
    var iceworm = {};

    iceworm.ServiceWebStatus = (function() {

        /**
         * Properties of a ServiceWebStatus.
         * @memberof iceworm
         * @interface IServiceWebStatus
         * @property {number|null} [uptime] ServiceWebStatus uptime
         */

        /**
         * Constructs a new ServiceWebStatus.
         * @memberof iceworm
         * @classdesc Represents a ServiceWebStatus.
         * @implements IServiceWebStatus
         * @constructor
         * @param {iceworm.IServiceWebStatus=} [properties] Properties to set
         */
        function ServiceWebStatus(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * ServiceWebStatus uptime.
         * @member {number} uptime
         * @memberof iceworm.ServiceWebStatus
         * @instance
         */
        ServiceWebStatus.prototype.uptime = 0;

        /**
         * Creates a new ServiceWebStatus instance using the specified properties.
         * @function create
         * @memberof iceworm.ServiceWebStatus
         * @static
         * @param {iceworm.IServiceWebStatus=} [properties] Properties to set
         * @returns {iceworm.ServiceWebStatus} ServiceWebStatus instance
         */
        ServiceWebStatus.create = function create(properties) {
            return new ServiceWebStatus(properties);
        };

        /**
         * Encodes the specified ServiceWebStatus message. Does not implicitly {@link iceworm.ServiceWebStatus.verify|verify} messages.
         * @function encode
         * @memberof iceworm.ServiceWebStatus
         * @static
         * @param {iceworm.IServiceWebStatus} message ServiceWebStatus message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ServiceWebStatus.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.uptime != null && Object.hasOwnProperty.call(message, "uptime"))
                writer.uint32(/* id 1, wireType 5 =*/13).float(message.uptime);
            return writer;
        };

        /**
         * Encodes the specified ServiceWebStatus message, length delimited. Does not implicitly {@link iceworm.ServiceWebStatus.verify|verify} messages.
         * @function encodeDelimited
         * @memberof iceworm.ServiceWebStatus
         * @static
         * @param {iceworm.IServiceWebStatus} message ServiceWebStatus message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        ServiceWebStatus.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a ServiceWebStatus message from the specified reader or buffer.
         * @function decode
         * @memberof iceworm.ServiceWebStatus
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {iceworm.ServiceWebStatus} ServiceWebStatus
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ServiceWebStatus.decode = function decode(reader, length) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.iceworm.ServiceWebStatus();
            while (reader.pos < end) {
                var tag = reader.uint32();
                switch (tag >>> 3) {
                case 1:
                    message.uptime = reader.float();
                    break;
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a ServiceWebStatus message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof iceworm.ServiceWebStatus
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {iceworm.ServiceWebStatus} ServiceWebStatus
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        ServiceWebStatus.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a ServiceWebStatus message.
         * @function verify
         * @memberof iceworm.ServiceWebStatus
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        ServiceWebStatus.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.uptime != null && message.hasOwnProperty("uptime"))
                if (typeof message.uptime !== "number")
                    return "uptime: number expected";
            return null;
        };

        /**
         * Creates a ServiceWebStatus message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof iceworm.ServiceWebStatus
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {iceworm.ServiceWebStatus} ServiceWebStatus
         */
        ServiceWebStatus.fromObject = function fromObject(object) {
            if (object instanceof $root.iceworm.ServiceWebStatus)
                return object;
            var message = new $root.iceworm.ServiceWebStatus();
            if (object.uptime != null)
                message.uptime = Number(object.uptime);
            return message;
        };

        /**
         * Creates a plain object from a ServiceWebStatus message. Also converts values to other types if specified.
         * @function toObject
         * @memberof iceworm.ServiceWebStatus
         * @static
         * @param {iceworm.ServiceWebStatus} message ServiceWebStatus
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        ServiceWebStatus.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults)
                object.uptime = 0;
            if (message.uptime != null && message.hasOwnProperty("uptime"))
                object.uptime = options.json && !isFinite(message.uptime) ? String(message.uptime) : message.uptime;
            return object;
        };

        /**
         * Converts this ServiceWebStatus to JSON.
         * @function toJSON
         * @memberof iceworm.ServiceWebStatus
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        ServiceWebStatus.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        return ServiceWebStatus;
    })();

    iceworm._Stub = (function() {

        /**
         * Properties of a _Stub.
         * @memberof iceworm
         * @interface I_Stub
         * @property {string|null} [data] _Stub data
         */

        /**
         * Constructs a new _Stub.
         * @memberof iceworm
         * @classdesc Represents a _Stub.
         * @implements I_Stub
         * @constructor
         * @param {iceworm.I_Stub=} [properties] Properties to set
         */
        function _Stub(properties) {
            if (properties)
                for (var keys = Object.keys(properties), i = 0; i < keys.length; ++i)
                    if (properties[keys[i]] != null)
                        this[keys[i]] = properties[keys[i]];
        }

        /**
         * _Stub data.
         * @member {string} data
         * @memberof iceworm._Stub
         * @instance
         */
        _Stub.prototype.data = "";

        /**
         * Creates a new _Stub instance using the specified properties.
         * @function create
         * @memberof iceworm._Stub
         * @static
         * @param {iceworm.I_Stub=} [properties] Properties to set
         * @returns {iceworm._Stub} _Stub instance
         */
        _Stub.create = function create(properties) {
            return new _Stub(properties);
        };

        /**
         * Encodes the specified _Stub message. Does not implicitly {@link iceworm._Stub.verify|verify} messages.
         * @function encode
         * @memberof iceworm._Stub
         * @static
         * @param {iceworm.I_Stub} message _Stub message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        _Stub.encode = function encode(message, writer) {
            if (!writer)
                writer = $Writer.create();
            if (message.data != null && Object.hasOwnProperty.call(message, "data"))
                writer.uint32(/* id 1, wireType 2 =*/10).string(message.data);
            return writer;
        };

        /**
         * Encodes the specified _Stub message, length delimited. Does not implicitly {@link iceworm._Stub.verify|verify} messages.
         * @function encodeDelimited
         * @memberof iceworm._Stub
         * @static
         * @param {iceworm.I_Stub} message _Stub message or plain object to encode
         * @param {$protobuf.Writer} [writer] Writer to encode to
         * @returns {$protobuf.Writer} Writer
         */
        _Stub.encodeDelimited = function encodeDelimited(message, writer) {
            return this.encode(message, writer).ldelim();
        };

        /**
         * Decodes a _Stub message from the specified reader or buffer.
         * @function decode
         * @memberof iceworm._Stub
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @param {number} [length] Message length if known beforehand
         * @returns {iceworm._Stub} _Stub
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        _Stub.decode = function decode(reader, length) {
            if (!(reader instanceof $Reader))
                reader = $Reader.create(reader);
            var end = length === undefined ? reader.len : reader.pos + length, message = new $root.iceworm._Stub();
            while (reader.pos < end) {
                var tag = reader.uint32();
                switch (tag >>> 3) {
                case 1:
                    message.data = reader.string();
                    break;
                default:
                    reader.skipType(tag & 7);
                    break;
                }
            }
            return message;
        };

        /**
         * Decodes a _Stub message from the specified reader or buffer, length delimited.
         * @function decodeDelimited
         * @memberof iceworm._Stub
         * @static
         * @param {$protobuf.Reader|Uint8Array} reader Reader or buffer to decode from
         * @returns {iceworm._Stub} _Stub
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        _Stub.decodeDelimited = function decodeDelimited(reader) {
            if (!(reader instanceof $Reader))
                reader = new $Reader(reader);
            return this.decode(reader, reader.uint32());
        };

        /**
         * Verifies a _Stub message.
         * @function verify
         * @memberof iceworm._Stub
         * @static
         * @param {Object.<string,*>} message Plain object to verify
         * @returns {string|null} `null` if valid, otherwise the reason why it is not
         */
        _Stub.verify = function verify(message) {
            if (typeof message !== "object" || message === null)
                return "object expected";
            if (message.data != null && message.hasOwnProperty("data"))
                if (!$util.isString(message.data))
                    return "data: string expected";
            return null;
        };

        /**
         * Creates a _Stub message from a plain object. Also converts values to their respective internal types.
         * @function fromObject
         * @memberof iceworm._Stub
         * @static
         * @param {Object.<string,*>} object Plain object
         * @returns {iceworm._Stub} _Stub
         */
        _Stub.fromObject = function fromObject(object) {
            if (object instanceof $root.iceworm._Stub)
                return object;
            var message = new $root.iceworm._Stub();
            if (object.data != null)
                message.data = String(object.data);
            return message;
        };

        /**
         * Creates a plain object from a _Stub message. Also converts values to other types if specified.
         * @function toObject
         * @memberof iceworm._Stub
         * @static
         * @param {iceworm._Stub} message _Stub
         * @param {$protobuf.IConversionOptions} [options] Conversion options
         * @returns {Object.<string,*>} Plain object
         */
        _Stub.toObject = function toObject(message, options) {
            if (!options)
                options = {};
            var object = {};
            if (options.defaults)
                object.data = "";
            if (message.data != null && message.hasOwnProperty("data"))
                object.data = message.data;
            return object;
        };

        /**
         * Converts this _Stub to JSON.
         * @function toJSON
         * @memberof iceworm._Stub
         * @instance
         * @returns {Object.<string,*>} JSON object
         */
        _Stub.prototype.toJSON = function toJSON() {
            return this.constructor.toObject(this, $protobuf.util.toJSONOptions);
        };

        return _Stub;
    })();

    return iceworm;
})();

module.exports = $root;
