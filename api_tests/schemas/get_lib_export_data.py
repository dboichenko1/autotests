GET_LIB_V1_CSHEMA={
  "$schema": "http://json-schema.org/draft-04/schema#",
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
          "items": [
            {
              "type": "object",
              "properties": {
                "docs": {
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
                                "info": {
                                  "type": "string"
                                },
                                "name": {
                                  "type": "string"
                                },
                                "type": {
                                  "type": "string"
                                }
                              },
                              "required": [
                                "info",
                                "name",
                                "type"
                              ]
                            }
                          ]
                        },
                        "desc": {
                          "type": "string"
                        },
                        "name": {
                          "type": "string"
                        },
                        "returnType": {
                          "type": "string"
                        },
                        "syntax": {
                          "type": "string"
                        }
                      },
                      "required": [
                        "args",
                        "desc",
                        "name",
                        "returnType",
                        "syntax"
                      ]
                    }
                  ]
                },
                "prefix": {
                  "type": "string"
                },
                "title": {
                  "type": "string"
                }
              },
              "required": [
                "docs",
                "prefix",
                "title"
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
  "$schema": "http://json-schema.org/draft-04/schema#",
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
                          "items": [
                            {
                              "type": "string"
                            },
                            {
                              "type": "string"
                            },
                            {
                              "type": "string"
                            },
                            {
                              "type": "string"
                            },
                            {
                              "type": "string"
                            },
                            {
                              "type": "string"
                            },
                            {
                              "type": "string"
                            },
                            {
                              "type": "string"
                            }
                          ]
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