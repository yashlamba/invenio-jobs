# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 CERN.
# Copyright (C) 2024 University of Münster.
#
# Invenio-Jobs is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Resources config."""

import marshmallow as ma
from flask_resources import HTTPJSONException, ResourceConfig, create_error_handler
from invenio_records_resources.resources.errors import ErrorHandlersMixin
from invenio_records_resources.resources.records.args import SearchRequestArgsSchema
from invenio_records_resources.services.base.config import ConfiguratorMixin

from ..services.errors import JobNotFoundError

response_handlers = {
    **ResourceConfig.response_handlers,
    "application/vnd.inveniordm.v1+json": ResourceConfig.response_handlers[
        "application/json"
    ],
}
request_body_parsers = {
    **ResourceConfig.request_body_parsers,
    "application/vnd.inveniordm.v1+json": ResourceConfig.request_body_parsers[
        "application/json"
    ],
}


class TasksResourceConfig(ResourceConfig, ConfiguratorMixin):
    """Celery tasks resource config."""

    # Blueprint configuration
    blueprint_name = "tasks"
    url_prefix = "/tasks"
    routes = {"list": ""}

    # Request handling
    request_search_args = SearchRequestArgsSchema
    request_body_parsers = request_body_parsers

    # Response handling
    response_handlers = response_handlers


class JobsSearchRequestArgsSchema(SearchRequestArgsSchema):
    """Jobs search request parameters."""

    active = ma.fields.Boolean()


class JobsResourceConfig(ResourceConfig, ConfiguratorMixin):
    """Jobs resource config."""

    # Blueprint configuration
    blueprint_name = "jobs"
    url_prefix = "/jobs"
    routes = {
        "list": "",
        "item": "/<job_id>",
    }

    # Request handling
    request_read_args = {}
    request_view_args = {"job_id": ma.fields.UUID()}
    request_search_args = JobsSearchRequestArgsSchema
    request_body_parsers = request_body_parsers

    # Response handling
    response_handlers = response_handlers

    error_handlers = {
        **ErrorHandlersMixin.error_handlers,
        JobNotFoundError: create_error_handler(
            lambda e: HTTPJSONException(code=404, description=e.description)
        ),
    }


class RunsResourceConfig(ResourceConfig, ConfiguratorMixin):
    """Runs resource config."""

    # Blueprint configuration
    blueprint_name = "job_runs"
    url_prefix = ""

    routes = {
        "list": "/jobs/<job_id>/runs",
        "item": "/jobs/<job_id>/runs/<run_id>",
        "logs_list": "/jobs/<job_id>/runs/<run_id>/logs",
        "actions_stop": "/jobs/<job_id>/runs/<run_id>/actions/stop",
    }

    # Request handling
    request_view_args = {
        "job_id": ma.fields.UUID(),
        "run_id": ma.fields.UUID(),
    }
    request_body_parsers = request_body_parsers

    # Response handling
    response_handlers = response_handlers

    error_handlers = {
        **ErrorHandlersMixin.error_handlers,
        # TODO: Add custom error handlers here
    }
