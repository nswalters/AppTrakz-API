""" Generate sankey diagram data """
import json
import sqlite3
from collections import Counter
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse

from apptrakzapi.views import Connection


def sankey(request):
    auth_token = request.headers["Authorization"].split(' ')[1]

    if request.method == 'GET':
        with sqlite3.connect(Connection.db_path) as conn:
            conn.row_factory = sqlite3.Row
            db_cursor = conn.cursor()

            # Get the applications statuses to use in Sankey diagram
            db_cursor.execute("""
                SELECT
                    application_id,
                    (SELECT user_id FROM authtoken_token WHERE key = ?) as uid,
                    CASE
                        WHEN
                            s.id = 1 then 'applied'
                        WHEN
                            s.id between 2 and 5 then 'interviewed'
                        WHEN
                            s.id = 6 then 'rejected'
                        WHEN
                            s.id = 7 then 'withdrew'
                        WHEN
                            s.id = 8 then 'offer'
                        WHEN
                            s.id = 9 then 'accepted'
                        WHEN
                            s.id = 10 then 'declined'
                    END AS node
                FROM
                    apptrakzapi_status as s
                JOIN
                    apptrakzapi_applicationstatus as app_stat
                        ON
                            app_stat.status_id = s.id
                JOIN
                    apptrakzapi_application as app
                        ON
                            app.id = app_stat.application_id
                WHERE
                    app.user_id = uid
                GROUP BY
                    application_id, node
                ORDER BY
                    application_id, created_at, node
            """, (auth_token, ))

            records = []
            dataset = db_cursor.fetchall()

            for row in dataset:
                record = {"app": row['application_id'], "node": row["node"]}
                records.append(record)

    results = make_sankey_data(records)

    return HttpResponse(json.dumps(results), content_type="application/json")


def create_nodes_array(data):
    """
    Receives:
        - Array of objects which indicate unique application statuses

        - Example:
            data = [{"app":1,"node":"applied"},{"app":2,"node":"applied"},{"app":2,"node":"interviewed"}]

    Returns:
        - Array of unique nodes objects with assigned node index

        - Example:
            nodes = [{'node': 0, 'name': 'applied'}, {'node': 1, 'name': 'interviewed'}, {'node': 2, 'name': 'rejected'}, {'node': 99, 'name': 'pending'}]
    """

    nodes = []
    node_index = 0

    for val in data:
        node = val["node"]

        if not list(filter(lambda x: x["name"] == node, nodes)):
            nodes.append({"node": node_index, "name": node})
            node_index += 1

    # add default 'pending' node
    nodes.append({"node": node_index, "name": "pending"})

    return nodes


def create_links_array(data, nodes):
    """
    Receives:  
        - [data] Array of objects which indicate unique application statuses
        - [nodes] Array of unique nodes objects with assigned node index

        - Example:
            data = [{"app":1,"node":"applied"},{"app":2,"node":"applied"},{"app":2,"node":"interviewed"}]

    Returns:
        - Array of unique link combinations and their respective counts
    """

    links_array = []

    for idx, val in enumerate(data):
        current_app = val['app']

        source_node = find_node_by_name(nodes, val['node'])['node']
        target_node = len(nodes) - 1  # default to pending

        # Terminating values which will never have a target assigned
        if val["node"] in ("rejected", "withdrew", "accepted", "declined"):
            continue

        # If we've reached the end, and it wasn't a terminating value,
        # append our default pending node then exit the loop
        if idx == len(data) - 1:
            links_array.append((source_node, target_node))
            break

        if data[idx + 1]['app'] == current_app:
            target_node = find_node_by_name(
                nodes, data[idx + 1]['node'])["node"]
            links_array.append((source_node, target_node))
        else:
            links_array.append((source_node, target_node))

    return links_array


def find_node_by_name(nodes_array, name):
    return list(filter(lambda x: x["name"] == name, nodes_array))[0]


def find_node_by_index(nodes_array, index):
    return list(filter(lambda x: x["node"] == index, nodes_array))[0]


def make_sankey_data(raw_data):
    nodes = create_nodes_array(raw_data)
    links = create_links_array(raw_data, nodes)

    link_records = []
    final_links = []

    for link in links:
        source_index = find_node_by_index(nodes, link[0])["node"]
        target_index = find_node_by_index(nodes, link[1])["node"]
        link_records.append((source_index, target_index))

    link_record_counts = Counter(link_records)

    for key, val in link_record_counts.items():
        final_links.append({"source": key[0], "target": key[1], "value": val})

    return {"nodes": nodes, "links": final_links}
