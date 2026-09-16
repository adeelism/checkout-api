# Checkout API

A simplified e-commerce checkout API. POST a list of product IDs, get back
the total price with bundle discounts applied.

## Setup

Requires Python 3.11+.

    python -m venv .venv
    source .venv/bin/activate        # Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    uvicorn app.main:app --port 8080 --reload

## Usage

Swagger UI: **http://localhost:8080/docs**

    curl -X POST http://localhost:8080/checkout \
      -H 'Content-Type: application/json' \
      -d '["001","002","001","004","003"]'
    # {"price":360}

## Tests

    pytest -v                    # everything
    pytest tests/unit -v         # pricing logic, no HTTP
    pytest tests/functional -v   # the endpoint end to end

## Catalogue

| ID  | Product        | Unit price | Offer      |
|-----|----------------|------------|------------|
| 001 | Silver Label   | $100       | 3 for $200 |
| 002 | Gold Label     | $80        | 2 for $120 |
| 003 | Platinum Label | $50        | —          |
| 004 | Diamond Label  | $30        | —          |

## Approach

The basket arrives as a flat list of IDs, so the first step is counting how
many of each product there are — `collections.Counter` does that in one pass.
Each product line is then priced independently and the results summed.

Offers are stored as a bundle quantity and a bundle price, not as a
percentage. "3 for $200" as a percentage is 33.333…%, which means floating
point, which means totals like $200.00000001. Storing `{"quantity": 3,
"price": 200}` keeps every operation in integers.

Pricing a line has no branching for whether the discount applies:

    bundles = quantity // offer["quantity"]
    remaining_units = quantity % offer["quantity"]
    return bundles * offer["price"] + remaining_units * unit_price

Floor division handles all three cases that look like they need separate
checks — below the bundle size gives zero bundles, an exact multiple gives
zero remainder, and anything in between splits naturally. My first version
had explicit guards for each of those and they were all redundant.

The pricing logic lives in `app/pricing.py` and knows nothing about HTTP.
`app/main.py` handles the request, calls it, and translates a domain error
into a status code. That's why the pricing tests don't import FastAPI.

## Assumptions

- **Remainders pay full price.** 4 Silver Labels = $200 + $100 = $300. The
  brief doesn't state this, but it's the only reading consistent with its own
  example, where 2 Silver Labels are charged at $200 rather than discounted.
- **An empty basket costs $0**, not an error. Nothing is malformed and there's
  nothing for the client to fix.
- **Unknown IDs are rejected, not skipped.** Silently dropping a typo'd ID
  returns a plausible but wrong total the client can't detect.
- **Prices are whole dollars**, so `int` is exact and serialises to the
  `{"price": 360}` shape the brief specifies.

## Errors

| Status | When                                           |
|--------|------------------------------------------------|
| 422    | Body isn't a JSON array of strings             |
| 400    | Body is valid but a product ID isn't in stock  |

## With more time

- Containerisation and a CI pipeline running lint and tests on every push.
- Money as integer cents. Whole-dollar prices made `int` safe here, but a
  real catalogue has fractional prices.
- A pricing-rule abstraction if a second kind of offer appeared (percentage
  off, buy-one-get-one). With one offer type there isn't enough information
  to design the right interface, so I didn't.
- The catalogue behind a repository rather than a module-level dict, once it
  comes from a database.
- A request size limit — a very large array is currently parsed in full
  before anything rejects it.
