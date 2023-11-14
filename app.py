from flask import Flask

import app_handler

app = Flask(__name__)


@app.route('/<path:relative_address_param>', methods=['GET'])
def get_normalized_page(relative_address_param: str):
    relative_address = relative_address_param
    if not relative_address.startswith("/"):
        relative_address = "/" + relative_address
    if relative_address in app_handler.normalized_pages:
        return str(app_handler.normalized_pages.get(relative_address))
    return ""


if __name__ == '__main__':
    app_handler.start_process()
    app.run(debug=False)
