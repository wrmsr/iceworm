/*eslint-disable block-scoped-var, id-length, no-control-regex, no-magic-numbers, no-prototype-builtins, no-redeclare, no-shadow, no-var, sort-vars*/
"use strict";

var $protobuf = require("protobufjs/light");

var $root = ($protobuf.roots["default"] || ($protobuf.roots["default"] = new $protobuf.Root()))
.addJSON({
  iceworm: {
    options: {
      java_package: "com.wrmsr.iceworm"
    },
    nested: {
      _Stub: {
        fields: {
          data: {
            type: "string",
            id: 1
          }
        }
      }
    }
  }
});

module.exports = $root;
