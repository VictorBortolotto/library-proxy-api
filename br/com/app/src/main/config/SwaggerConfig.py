from flasgger import Swagger

class SwaggerConfig:
  def config(self, app):
    swagger_config = {
      "headers": [],
      "specs": [
          {
              "endpoint": "apispec",
              "route": "/apispec.json",
              "rule_filter": lambda rule: True,
              "model_filter": lambda tag: True,
          }
      ],
      "static_url_path": "/flasgger_static",
      "swagger_ui": True,
      "specs_route": "/apidocs/",
      "swagger_ui_bundle_js": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui-bundle.js",
      "swagger_ui_standalone_preset_js": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui-standalone-preset.js",
      "swagger_ui_css": "https://cdn.jsdelivr.net/npm/swagger-ui-dist/swagger-ui.css",
    }
    return Swagger(app, config=swagger_config)

