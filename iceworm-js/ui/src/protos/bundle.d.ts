import * as $protobuf from "protobufjs";
/** Namespace iceworm. */
export namespace iceworm {

    /** Properties of a ServiceWebStatus. */
    interface IServiceWebStatus {

        /** ServiceWebStatus uptime */
        uptime?: (number|null);
    }

    /** Represents a ServiceWebStatus. */
    class ServiceWebStatus implements IServiceWebStatus {

        /**
         * Constructs a new ServiceWebStatus.
         * @param [properties] Properties to set
         */
        constructor(properties?: iceworm.IServiceWebStatus);

        /** ServiceWebStatus uptime. */
        public uptime: number;

        /**
         * Creates a new ServiceWebStatus instance using the specified properties.
         * @param [properties] Properties to set
         * @returns ServiceWebStatus instance
         */
        public static create(properties?: iceworm.IServiceWebStatus): iceworm.ServiceWebStatus;

        /**
         * Encodes the specified ServiceWebStatus message. Does not implicitly {@link iceworm.ServiceWebStatus.verify|verify} messages.
         * @param message ServiceWebStatus message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: iceworm.IServiceWebStatus, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified ServiceWebStatus message, length delimited. Does not implicitly {@link iceworm.ServiceWebStatus.verify|verify} messages.
         * @param message ServiceWebStatus message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: iceworm.IServiceWebStatus, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a ServiceWebStatus message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns ServiceWebStatus
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): iceworm.ServiceWebStatus;

        /**
         * Decodes a ServiceWebStatus message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns ServiceWebStatus
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): iceworm.ServiceWebStatus;

        /**
         * Verifies a ServiceWebStatus message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a ServiceWebStatus message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns ServiceWebStatus
         */
        public static fromObject(object: { [k: string]: any }): iceworm.ServiceWebStatus;

        /**
         * Creates a plain object from a ServiceWebStatus message. Also converts values to other types if specified.
         * @param message ServiceWebStatus
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: iceworm.ServiceWebStatus, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this ServiceWebStatus to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };
    }

    /** Properties of a _Stub. */
    interface I_Stub {

        /** _Stub data */
        data?: (string|null);
    }

    /** Represents a _Stub. */
    class _Stub implements I_Stub {

        /**
         * Constructs a new _Stub.
         * @param [properties] Properties to set
         */
        constructor(properties?: iceworm.I_Stub);

        /** _Stub data. */
        public data: string;

        /**
         * Creates a new _Stub instance using the specified properties.
         * @param [properties] Properties to set
         * @returns _Stub instance
         */
        public static create(properties?: iceworm.I_Stub): iceworm._Stub;

        /**
         * Encodes the specified _Stub message. Does not implicitly {@link iceworm._Stub.verify|verify} messages.
         * @param message _Stub message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: iceworm.I_Stub, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified _Stub message, length delimited. Does not implicitly {@link iceworm._Stub.verify|verify} messages.
         * @param message _Stub message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: iceworm.I_Stub, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a _Stub message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns _Stub
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): iceworm._Stub;

        /**
         * Decodes a _Stub message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns _Stub
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): iceworm._Stub;

        /**
         * Verifies a _Stub message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a _Stub message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns _Stub
         */
        public static fromObject(object: { [k: string]: any }): iceworm._Stub;

        /**
         * Creates a plain object from a _Stub message. Also converts values to other types if specified.
         * @param message _Stub
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: iceworm._Stub, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this _Stub to JSON.
         * @returns JSON object
         */
        public toJSON(): { [k: string]: any };
    }
}
