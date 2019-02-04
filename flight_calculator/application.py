from envi import Application
from controllers import RoutesController

application = Application()
application.route("/<action>/", RoutesController)      # latest version of the controller
application.route("/v1/<action>/", RoutesController)   # specific version of the controller
