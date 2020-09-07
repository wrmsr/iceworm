import * as $protobuf from "protobufjs";
/** Namespace iceworm. */
export namespace iceworm {

    /** Properties of a WebServiceStatus. */
    interface IWebServiceStatus {

        /** WebServiceStatus uptime */
        uptime?: (number|null);
    }

    /** Represents a WebServiceStatus. */
    class WebServiceStatus implements IWebServiceStatus {

        /**
         * Constructs a new WebServiceStatus.
         * @param [properties] Properties to set
         */
        constructor(properties?: iceworm.IWebServiceStatus);

        /** WebServiceStatus uptime. */
        public uptime: number;

        /**
         * Creates a new WebServiceStatus instance using the specified properties.
         * @param [properties] Properties to set
         * @returns WebServiceStatus instance
         */
        public static create(properties?: iceworm.IWebServiceStatus): iceworm.WebServiceStatus;

        /**
         * Encodes the specified WebServiceStatus message. Does not implicitly {@link iceworm.WebServiceStatus.verify|verify} messages.
         * @param message WebServiceStatus message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encode(message: iceworm.IWebServiceStatus, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Encodes the specified WebServiceStatus message, length delimited. Does not implicitly {@link iceworm.WebServiceStatus.verify|verify} messages.
         * @param message WebServiceStatus message or plain object to encode
         * @param [writer] Writer to encode to
         * @returns Writer
         */
        public static encodeDelimited(message: iceworm.IWebServiceStatus, writer?: $protobuf.Writer): $protobuf.Writer;

        /**
         * Decodes a WebServiceStatus message from the specified reader or buffer.
         * @param reader Reader or buffer to decode from
         * @param [length] Message length if known beforehand
         * @returns WebServiceStatus
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decode(reader: ($protobuf.Reader|Uint8Array), length?: number): iceworm.WebServiceStatus;

        /**
         * Decodes a WebServiceStatus message from the specified reader or buffer, length delimited.
         * @param reader Reader or buffer to decode from
         * @returns WebServiceStatus
         * @throws {Error} If the payload is not a reader or valid buffer
         * @throws {$protobuf.util.ProtocolError} If required fields are missing
         */
        public static decodeDelimited(reader: ($protobuf.Reader|Uint8Array)): iceworm.WebServiceStatus;

        /**
         * Verifies a WebServiceStatus message.
         * @param message Plain object to verify
         * @returns `null` if valid, otherwise the reason why it is not
         */
        public static verify(message: { [k: string]: any }): (string|null);

        /**
         * Creates a WebServiceStatus message from a plain object. Also converts values to their respective internal types.
         * @param object Plain object
         * @returns WebServiceStatus
         */
        public static fromObject(object: { [k: string]: any }): iceworm.WebServiceStatus;

        /**
         * Creates a plain object from a WebServiceStatus message. Also converts values to other types if specified.
         * @param message WebServiceStatus
         * @param [options] Conversion options
         * @returns Plain object
         */
        public static toObject(message: iceworm.WebServiceStatus, options?: $protobuf.IConversionOptions): { [k: string]: any };

        /**
         * Converts this WebServiceStatus to JSON.
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
