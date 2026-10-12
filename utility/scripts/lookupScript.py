
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from datetime import datetime
from mongoengine import connect
# from ...domain.models.Lookup import Lookup

# from ..helper.constants import Lookups
# from ..helper.lookups import DESIGNATION, USER_TYPE, TOKEN_TYPE, CITY
from domain.models.Lookup import Lookup
from utility.helper.constant import Lookups
from utility.helper.lookup import DESIGNATION, USER_TYPE, TOKEN_TYPE, CASE_TYPE, CASE_PRIORITY, CASE_STATUS, CASE_ROLE, CASE_DOCUMENT_TYPE, CASE_NOTE_TYPE, BILLING_STATUS,CASE_DIARY_TYPE

connect("legal_ai_db")



def upsert_lookup(id, parent_id, name, value):

    existing = Lookup.objects(id=id).first()

    if not existing:
        Lookup(
            id=id,
            parent=Lookup.objects(id=parent_id).first() if parent_id else None,
            name=name,
            value=value,
            created_on=datetime.utcnow(),
            updated_on=datetime.utcnow(),
        ).save()
        print(f"Inserted: {name}")
    else:
        print(f"Exists: {name}")


def seed():


    upsert_lookup(Lookups.DESIGNATION, None, "Designation", "DE")
   # upsert_lookup(Lookups.CITY, None, "City", "CS")
    upsert_lookup(Lookups.USER_TYPE, None, "User type", "UT")
    upsert_lookup(Lookups.TOKEN_TYPE, None, "Token Type", "TT")
    upsert_lookup(DESIGNATION.ADVOCATE_HIGH_COURT, Lookups.DESIGNATION, "Advocate High Court", "AD_1")
    upsert_lookup(DESIGNATION.ADVOCATE_DISTRICT_COURT, Lookups.DESIGNATION, "Advocate District Court", "AD_2")
    upsert_lookup(USER_TYPE.ADMIN, Lookups.USER_TYPE, "Admin", "US_1")
    upsert_lookup(USER_TYPE.USER, Lookups.USER_TYPE, "User", "US_2")
    upsert_lookup(TOKEN_TYPE.JWT, Lookups.TOKEN_TYPE, "JWT Token", "TO_1")
    # CASE TYPE
    upsert_lookup(CASE_TYPE.CIVIL, Lookups.CASE_TYPE, "Civil", "CT_1")
    upsert_lookup(CASE_TYPE.CRIMINAL, Lookups.CASE_TYPE, "Criminal", "CT_2")
    upsert_lookup(CASE_TYPE.CONSTITUTIONAL, Lookups.CASE_TYPE, "Constitutional", "CT_3")
    upsert_lookup(CASE_TYPE.FAMILY, Lookups.CASE_TYPE, "Family", "CT_4")
    upsert_lookup(CASE_TYPE.TAX_REVENUE, Lookups.CASE_TYPE, "Tax / Revenue", "CT_5")
    upsert_lookup(CASE_TYPE.BANKING, Lookups.CASE_TYPE, "Banking", "CT_6")
    upsert_lookup(CASE_TYPE.LABOUR, Lookups.CASE_TYPE, "Labour", "CT_7")
    upsert_lookup(CASE_TYPE.CORPORATE, Lookups.CASE_TYPE, "Corporate", "CT_8")
    upsert_lookup(CASE_TYPE.NAB, Lookups.CASE_TYPE, "NAB", "CT_9")
    upsert_lookup(CASE_TYPE.CUSTOMS, Lookups.CASE_TYPE, "Customs", "CT_10")


    # CASE PRIORITY
    upsert_lookup(CASE_PRIORITY.MEDIUM, Lookups.CASE_PRIORITY, "Medium", "CP_1")
    upsert_lookup(CASE_PRIORITY.HIGH, Lookups.CASE_PRIORITY, "High", "CP_2")
    upsert_lookup(CASE_PRIORITY.URGENT, Lookups.CASE_PRIORITY, "Urgent", "CP_3")
    upsert_lookup(CASE_PRIORITY.LOW, Lookups.CASE_PRIORITY, "Low", "CP_4")


    # CASE STATUS
    upsert_lookup(CASE_STATUS.ACTIVE, Lookups.CASE_STATUS, "Active", "CS_1")
    upsert_lookup(CASE_STATUS.PENDING, Lookups.CASE_STATUS, "Pending", "CS_2")
    upsert_lookup(CASE_STATUS.STAYED, Lookups.CASE_STATUS, "Stayed", "CS_3")
    upsert_lookup(CASE_STATUS.RESERVED, Lookups.CASE_STATUS, "Reserved", "CS_4")
    upsert_lookup(CASE_STATUS.DISPOSED, Lookups.CASE_STATUS, "Disposed", "CS_5")


    # CASE ROLE
    upsert_lookup(CASE_ROLE.PETITIONER, Lookups.CASE_ROLE, "Petitioner", "CR_1")
    upsert_lookup(CASE_ROLE.RESPONDENT, Lookups.CASE_ROLE, "Respondent", "CR_2")
    upsert_lookup(CASE_ROLE.PLAINTIFF, Lookups.CASE_ROLE, "Plaintiff", "CR_3")
    upsert_lookup(CASE_ROLE.DEFENDENT, Lookups.CASE_ROLE, "Defendant", "CR_4")
    upsert_lookup(CASE_ROLE.APPLICANT, Lookups.CASE_ROLE, "Applicant", "CR_5")
    upsert_lookup(CASE_ROLE.COMPLAINANT, Lookups.CASE_ROLE, "Complainant", "CR_6")
    upsert_lookup(CASE_ROLE.ACCUSED, Lookups.CASE_ROLE, "Accused", "CR_7")
    upsert_lookup(CASE_ROLE.APPELLANT, Lookups.CASE_ROLE, "Appellant", "CR_8")
    upsert_lookup(CASE_ROLE.OPPOSITE_PARTY, Lookups.CASE_ROLE, "Opposite Party", "CR_9")



    # CASE DOCUMENT TYPE
    upsert_lookup(CASE_DOCUMENT_TYPE.PLAINT, Lookups.CASE_DOCUMENT_TYPE, "Plaint", "CD_1")
    upsert_lookup(CASE_DOCUMENT_TYPE.WRITTEN_STATEMENT, Lookups.CASE_DOCUMENT_TYPE, "Written Statement", "CD_2")
    upsert_lookup(CASE_DOCUMENT_TYPE.APPLICATION, Lookups.CASE_DOCUMENT_TYPE, "Application", "CD_3")
    upsert_lookup(CASE_DOCUMENT_TYPE.ORDER, Lookups.CASE_DOCUMENT_TYPE, "Order", "CD_4")
    upsert_lookup(CASE_DOCUMENT_TYPE.JUDGMENT, Lookups.CASE_DOCUMENT_TYPE, "Judgment", "CD_5")
    upsert_lookup(CASE_DOCUMENT_TYPE.AFFIDAVIT, Lookups.CASE_DOCUMENT_TYPE, "Affidavit", "CD_6")
    upsert_lookup(CASE_DOCUMENT_TYPE.VAKALATNAMA, Lookups.CASE_DOCUMENT_TYPE, "Vakalatnama", "CD_7")
    upsert_lookup(CASE_DOCUMENT_TYPE.OTHER, Lookups.CASE_DOCUMENT_TYPE, "Other", "CD_8")


    # CASE NOTE TYPE
    upsert_lookup(CASE_NOTE_TYPE.GENERAL_NOTE, Lookups.CASE_NOTE_TYPE, "General Note", "CN_1")
    upsert_lookup(CASE_NOTE_TYPE.COURT_ORDER, Lookups.CASE_NOTE_TYPE, "Court Order", "CN_2")
    upsert_lookup(CASE_NOTE_TYPE.CLIENT_COMMUNICATION, Lookups.CASE_NOTE_TYPE, "Client Communication", "CN_3")
    upsert_lookup(CASE_NOTE_TYPE.STRATEGY, Lookups.CASE_NOTE_TYPE, "Strategy", "CN_4")
    upsert_lookup(CASE_NOTE_TYPE.COURT_PROCEEDING, Lookups.CASE_NOTE_TYPE, "Court Proceeding", "CN_5")


    # BILLING STATUS
    upsert_lookup(BILLING_STATUS.PAID, Lookups.BILLING_STATUS, "Paid", "BS_1")
    upsert_lookup(BILLING_STATUS.UNPAID, Lookups.BILLING_STATUS, "Unpaid", "BS_2")
    upsert_lookup(BILLING_STATUS.PARTIAL, Lookups.BILLING_STATUS, "Partial", "BS_3")
    #Case diary type
    upsert_lookup(CASE_DIARY_TYPE.HEARING, Lookups.CASE_DIARY_TYPE, "Hearing", "CDT_1")
    upsert_lookup(CASE_DIARY_TYPE.EVIDENCE, Lookups.CASE_DIARY_TYPE, "Evidence", "CDT_2")
    upsert_lookup(CASE_DIARY_TYPE.ARGUMENTS, Lookups.CASE_DIARY_TYPE, "Arguments", "CDT_3")
    upsert_lookup(CASE_DIARY_TYPE.JUDGEMENT, Lookups.CASE_DIARY_TYPE, "Judgement", "CDT_4")
    upsert_lookup(CASE_DIARY_TYPE.ORDER, Lookups.CASE_DIARY_TYPE, "Order", "CDT_5")
    upsert_lookup(CASE_DIARY_TYPE.FILING_DEADLINE, Lookups.CASE_DIARY_TYPE, "Filing Deadline", "CDT_6")
    upsert_lookup(CASE_DIARY_TYPE.LIMITATION_ALERT, Lookups.CASE_DIARY_TYPE, "Limitation Alert", "CDT_7")
    upsert_lookup(CASE_DIARY_TYPE.ADJOURNMENT, Lookups.CASE_DIARY_TYPE, "Adjournment", "CDT_8")
    upsert_lookup(CASE_DIARY_TYPE.MEETING, Lookups.CASE_DIARY_TYPE, "Meeting", "CDT_9")

    print("Lookup seeding completed safely ✅")


if __name__ == "__main__":
    seed()