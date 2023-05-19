from django import template


# Create Register instance
register = template.Library()


# Changing price(Rials to Tooman)
@register.filter
def changing(value):
    value = str(value)
    return int(value[:-1])


# Intcomma filter(prices, discounts, ...)
@register.filter
def intcomma(value):
    return "{:,}".format(value)


# Calculate price discount
@register.filter
def discount(value, price):
    return price - value
