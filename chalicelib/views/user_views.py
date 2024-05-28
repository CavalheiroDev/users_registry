import uuid

from chalice import Response, Blueprint
from chalicelib.repositories.user_repository import user_repository
from chalicelib.schemas.user_input_schema import UserInputSchema

user_router = Blueprint(__name__)


# FAZER MIDDLEWARE PARA LIDAR COM marshmallow.exceptions.ValidationError
@user_router.route('/', methods=['POST'], content_types=['application/json'], cors=True)
def create_user():
    request_body = user_router.current_request.json_body

    schema = UserInputSchema(data=request_body)
    schema.is_valid(raise_exception=True)

    try:
        response = user_repository.create_item(
            pk=str(uuid.uuid4()),
            item=schema.data
        )

        return Response(
            body=response,
            status_code=201
        )

    except Exception as error:
        user_router.log.exception(error)
        return Response(
            body={'message': 'An error occurred when creating the user.'},
            status_code=500
        )


@user_router.route('/', methods=['GET'], content_types=['application/json'], cors=True)
def list_users():
    response = user_repository.list_items()

    return {'results': response}


@user_router.route('/{user_id}', methods=['GET'], content_types=['application/json'], cors=True)
def retrieve_user(user_id: str):
    response = user_repository.find_by_id(pk=user_id)
    if not response:
        return Response(
            body={'message': 'User not found.'},
            status_code=400
        )

    return response[0]


@user_router.route('/{user_id}', methods=['PUT'], content_types=['application/json'], cors=True)
def update_user(user_id: str):
    request_body = user_router.current_request.json_body

    schema = UserInputSchema(data=request_body)
    schema.is_valid(raise_exception=True)

    try:
        response = user_repository.update_item(pk=user_id,
                                               email=schema.data['email'],
                                               username=schema.data['username'])

        return Response(
            body=response.get('Attributes'),
            status_code=202
        )

    except Exception as error:
        user_router.log.exception(error)
        return Response(
            body={'message': 'An error occurred when updating the user.'},
            status_code=500
        )


@user_router.route('/{user_id}', methods=['DELETE'], content_types=['application/json'], cors=True)
def delete_user(user_id: str):
    try:
        user_repository.delete_item(pk=user_id)

        return Response(
            body={},
            status_code=204
        )

    except Exception as error:
        user_router.log.exception(error)
        return Response(
            body={'message': 'An error occurred when deleting a user.'},
            status_code=500
        )
