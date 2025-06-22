from flask import views
from flask_smorest import Blueprint, abort
from marshmallow import Schema, fields, validate
from flask_jwt_extended import jwt_required
import datetime as dt
from decimal import Decimal
import uuid

example = Blueprint(
    "example",
    "example",
    url_prefix="/example",
    description="Flask smorest blueprint example to create invoices",
)

# Sample data for demonstration purposes
invoices = [
    {
        "customer": {"name": "John Doe"},
        "payment": {
            "id": "PAY-0001",
            "amount": Decimal(100),
            "date": dt.datetime.now(dt.timezone.utc),
        },
        "id": uuid.UUID("0ef3807d-7459-405e-a555-fe1d00bb848c"),
    }
]


class Customer(Schema):
    name = fields.String(required=True, description="Name of the customer")


class Payment(Schema):
    id = fields.String(required=True, description="Unique identifier for the payment")
    amount = fields.Decimal(
        as_string=True,
        required=True,
        description="Amount of the payment",
        validate=validate.Range(min=0),
    )
    date = fields.DateTime(required=True, description="Date of the payment")


class CreateInvoice(Schema):
    customer = fields.Nested(Customer, required=True, description="Customer details")
    payment = fields.Nested(
        Payment, required=True, description="Payment associated with the invoice"
    )


class Invoice(CreateInvoice):
    id = fields.UUID(required=True, description="Unique identifier for the invoice")


class ListInvoices(Schema):
    invoices = fields.List(
        fields.Nested(Invoice), required=True, description="List of invoices"
    )


@example.route("/invoices", methods=["GET", "POST"])
class InvoiceCollection(views.MethodView):

    @jwt_required()
    @example.response(200, ListInvoices)
    def get(self):
        """List all invoices"""
        return {"invoices": invoices}

    @jwt_required()
    @example.arguments(CreateInvoice)
    @example.response(201, Invoice)
    def post(self, invoice):
        """Create a new invoice"""
        new_invoice = {
            "id": uuid.uuid4(),
            "customer": invoice["customer"],
            "payment": invoice["payment"],
        }
        invoices.append(new_invoice)
        return new_invoice


@example.route("/invoices/<uuid:invoice_id>", methods=["GET"])
class InvoiceSingleton(views.MethodView):

    @jwt_required()
    @example.response(200, Invoice)
    def get(self, invoice_id):
        """Get a specific invoice by ID"""
        for inv in invoices:
            if inv["id"] == invoice_id:
                return inv
        abort(404, message="Invoice not found")
