from sanic.response import json
from sanic import Blueprint
from sanic_openapi import doc
from Decorators import permission
from Query.announce import Announce

announcement = Blueprint('announcement')


@doc.summary("Get 5 announcement, use page to get next 5 data")
@doc.consumes({"page": int}, location='query', required=True)
@doc.produces(
    {'title': str, 'post_time': int, 'last_edit_time': int, 'content': str,
     'delete_count': int, 'poster_id': str, 'top': int},
    content_type='application/json')
@announcement.route('/announcement', methods=['GET'])
@permission("4600")
async def bp_announcement(request, *args, **kwargs):
    try:
        page = int(request.args['page'][0])
        query = Announce()
        data = query.get_announcement(page)
        response = json(data)

    except ValueError:
        return json("bad request", 400)
    except KeyError:
        return json("bad request", 400)

    return response


@announcement.route('/announcement/<post_id>', methods=['GET'])
async def bp_single_announcement(request, post_id):
    response = json({})
    return response
