from typing import Any, Optional

from blacksheep import Request, Response
from blacksheep.server.controllers import Controller
from blacksheep.server.templating import get_response, render_template_async, template_name, model_to_view_params


class BaseController(Controller):
    async def view_async(self, name: Optional[str] = None, model: Optional[Any] = None,
                         request: Request = None) -> Response:
        if isinstance(model, dict):
            model['requestuser'] = request.identity.get_user_form()  # type: ignore
        else:
            model = {'requestuser': request.identity.get_user_form()}  # type: ignore
        return await super(BaseController, self).view_async(name=name, model=model)

    @classmethod
    def class_name(cls) -> str:
        return cls.__name__.lower().replace('controller', '')

    def full_view_name(self, name: str) -> str:
        return f"{self.class_name()}/{name}"


async def view_async(
        name: str, model: Any = None, request: Request = None
) -> Response:
    """
    Returns a Response object with HTML obtained from synchronous rendering.
    """
    from server import app

    jinja_environment = app.jinja_environment
    if model:
        if isinstance(model, dict):
            model['requestuser'] = request.identity.get_user_form()  # type: ignore
        else:
            model = {'requestuser': request.identity.get_user_form()}  # type: ignore
        return get_response(
            await render_template_async(
                jinja_environment.get_template(template_name(name)),
                **model_to_view_params(model)
            )
        )
    return get_response(
        await render_template_async(jinja_environment.get_template(template_name(name)))
    )


async def delete(request: Request, name: str, data=None) -> Response:
    if data is None:
        data = []
    return await view_async(
        'common/delete',
        model={
            'name': name,
            'data': data,
        },
        request=request
    )
