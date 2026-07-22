def recommend(carbon):

    if carbon < 20:

        category = "Low"

        suggestion = """
Excellent! 🌱
Your carbon footprint is very low.
Keep using public transport, save electricity,
and continue your eco-friendly lifestyle.
"""

    elif carbon < 50:

        category = "Medium"

        suggestion = """
Good 👍
Your carbon footprint is moderate.
Try reducing electricity usage,
avoid single-use plastics,
and plant more trees.
"""

    else:

        category = "High"

        suggestion = """
Warning! ⚠️
Your carbon footprint is high.
Use public transport,
reduce fuel consumption,
save electricity,
and recycle more waste.
"""

    return category, suggestion