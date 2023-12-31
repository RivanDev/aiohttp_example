import uuid

from aiohttp.web_exceptions import HTTPNotFound

from aiohttp_apispec import docs, request_schema, response_schema, querystring_schema

from app.crm.models import User
from app.crm.schemes import UserSchema, ListUsersResponseSchema, UserGetRequestSchema, UserGetResponseSchema
from app.web.app import View
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response


class AddUserView(View):
    @docs(tags=['crm'], summary='Add new user', description='Add new user to database')
    @request_schema(UserSchema)
    @response_schema(OkResponseSchema, 200)
    async def post(self):
        data = await self.request.json()
        user = User(email=data['email'], id_=uuid.uuid4())
        await self.request. app.crm_accessor.add_user(user)
        return json_response()


class ListUsersView(View):
    @docs(tags=['crm'], summary='List users', description='List users from database')
    @response_schema(ListUsersResponseSchema, 200)
    async def get(self):
        users = await self.request.app.crm_accessor.list_users()
        raw_users = [{'email': user.email, 'id': str(user.id_)} for user in users]
        return json_response(data={'users': raw_users})


class GetUserView(View):
    @docs(tags=['crm'], summary='Get user', description='Get user from database')
    @querystring_schema(UserGetRequestSchema)
    @response_schema(UserGetResponseSchema, 200)
    async def get(self):
        user_id = self.request.query['id']
        user = await self.request.app.crm_accessor.get_user(uuid.UUID(user_id))
        if user:
            return json_response(data={'user': {'email': user.email, 'id': str(user.id_)}})
        else:
            raise HTTPNotFound
