GET_LIB_V1_CSHEMA={
  "type": "object",
  "properties": {
    "libInfo": {
      "type": "object",
      "properties": {
        "user": {
          "type": "string"
        },
        "userId": {
          "type": "integer"
        },
        "scriptIdPart": {
          "type": "string"
        },
        "version": {
          "type": "string"
        },
        "docs": {
          "type": "string"
        },
        "chartId": {
          "type": "string"
        },
        "isPublic": {
          "type": "boolean"
        },
        "lib": {
          "type": "string"
        },
        "libId": {
          "type": "string"
        }
      },
      "required": [
        "user",
        "userId",
        "scriptIdPart",
        "version",
        "docs",
        "chartId",
        "isPublic",
        "lib",
        "libId"
      ]
    },
    "exports": {
      "type": "object",
      "properties": {
        "functions2": {
          "type": "array",
        },
        "types": {
          "type": "array",
          "items": {}
        }
      },
      "required": [
        "functions2",
        "types"
      ]
    }
  },
  "required": [
    "libInfo",
    "exports"
  ]
}

GET_LIB_V2_CSHEMA = {
  "type": "object",
  "properties": {
    "libInfo": {
      "type": "object",
      "properties": {
        "user": {
          "type": "string"
        },
        "userId": {
          "type": "integer"
        },
        "scriptIdPart": {
          "type": "string"
        },
        "version": {
          "type": "string"
        },
        "docs": {
          "type": "string"
        },
        "chartId": {
          "type": "string"
        },
        "isPublic": {
          "type": "boolean"
        },
        "lib": {
          "type": "string"
        },
        "libId": {
          "type": "string"
        }
      },
      "required": [
        "user",
        "userId",
        "scriptIdPart",
        "version",
        "docs",
        "chartId",
        "isPublic",
        "lib",
        "libId"
      ]
    },
    "exports": {
      "type": "object",
      "properties": {
        "functions": {
          "type": "array",
          "items": [
            {
              "type": "object",
              "properties": {
                "args": {
                  "type": "array",
                  "items": [
                    {
                      "type": "object",
                      "properties": {
                        "allowedTypeIDs": {
                          "type": "array",
                        },
                        "desc": {
                          "type": "string"
                        },
                        "displayType": {
                          "type": "string"
                        },
                        "name": {
                          "type": "string"
                        },
                        "required": {
                          "type": "boolean"
                        }
                      },
                      "required": [
                        "allowedTypeIDs",
                        "desc",
                        "displayType",
                        "name",
                        "required"
                      ]
                    }
                  ]
                },
                "desc": {
                  "type": "array",
                  "items": [
                    {
                      "type": "string"
                    }
                  ]
                },
                "libId": {
                  "type": "string"
                },
                "name": {
                  "type": "string"
                },
                "returnedTypes": {
                  "type": "array",
                  "items": [
                    {
                      "type": "string"
                    }
                  ]
                },
                "returns": {
                  "type": "array",
                  "items": [
                    {
                      "type": "string"
                    }
                  ]
                },
                "syntax": {
                  "type": "array",
                  "items": [
                    {
                      "type": "string"
                    }
                  ]
                }
              },
              "required": [
                "args",
                "desc",
                "libId",
                "name",
                "returnedTypes",
                "returns",
                "syntax"
              ]
            }
          ]
        },
        "types": {
          "type": "array",
          "items": {}
        }
      },
      "required": [
        "functions",
        "types"
      ]
    }
  },
  "required": [
    "libInfo",
    "exports"
  ]
}