# class Acronym:
#     def __init__(self, reduction, transcript, subcategory_name: str):
#         self.reduction = reduction
#         self.transcript = transcript
#         self.subcategory_name = subcategory_name
#         self.db = db
#
#     def __str__(self):
#         return f"{self.reduction} - {self.transcript}"
#
#     def write(self):
#         from sqlalchemy import select
#
#         acronyms = self.db.acronyms
#         subcategories = self.db.subcategories
#         conn = self.db.engine.connect()
#
#         conn.execute(
#             acronyms.insert().values(
#                 reduction=self.reduction,
#                 transcript=self.transcript,
#                 subcategory_id=conn.execute(select([subcategories]).where(
#                     subcategories.c.name == self.subcategory_name
#                 )).fetchone().id
#             )
#         )
