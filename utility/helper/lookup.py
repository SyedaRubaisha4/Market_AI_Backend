import uuid

class DESIGNATION:
    ADVOCATE_HIGH_COURT = str(uuid.UUID("ca229534-268c-4961-b199-da82b76c03a2"))
    ADVOCATE_DISTRICT_COURT = str(uuid.UUID("38c66be2-6047-4d96-acce-663f26d97485"))
    # ADVOCATE_SUPREME_COURT = uuid.UUID("22222222-0000-0000-0000-000000000003")
    # CORPORATE_IN_HOUSE = uuid.UUID("22222222-0000-0000-0000-000000000004")
    # JUDGE = uuid.UUID("22222222-0000-0000-0000-000000000005")
    # LAW_STUDENT = uuid.UUID("22222222-0000-0000-0000-000000000006")
    # LEGAL_ACADEMICE = uuid.UUID("22222222-0000-0000-0000-000000000007")
    # NGO_FOUNDER = uuid.UUID("22222222-0000-0000-0000-000000000008")
    # OTHER = uuid.UUID("22222222-0000-0000-0000-000000000008")




class USER_TYPE:
    ADMIN = str(uuid.UUID("05196076-2df2-46a1-afad-13f8dc22e8c3"))
    USER = str(uuid.UUID("db0e1b8b-f9b0-4aa8-b048-3b0ea5492fa6"))
    

class TOKEN_TYPE:
    JWT = str(uuid.UUID("68db2b46-a88a-483b-9d5a-240fd9caca7e"))





class CASE_TYPE:
    CIVIL = str(uuid.UUID("d87ac57f-1d18-42e3-a9de-3f148e5355f2"))
    CRIMINAL = str(uuid.UUID("979c8c0d-8b61-4b43-8366-41533d438e2f"))
    CONSTITUTIONAL = str(uuid.UUID("c549e9b6-cb01-42d8-8aa2-e26bc034a08f"))
    FAMILY = str(uuid.UUID("1a24ee7b-af4e-4d26-88b1-b8525d89095c"))
    TAX_REVENUE = str(uuid.UUID("ff3caf4a-4fc9-43af-8aa7-f0db3cb300eb"))
    BANKING = str(uuid.UUID("98f563f8-7439-4061-9666-e652fff641b7"))
    LABOUR = str(uuid.UUID("fc7c89eb-fb01-4bbf-a67d-b95527abd7c0"))
    CORPORATE = str(uuid.UUID("ba9fe526-af04-4d6b-8743-5e339278c90f"))
    NAB = str(uuid.UUID("bc81bdbe-8677-4a1d-bded-fa7b0f9a922d"))
    CUSTOMS = str(uuid.UUID("c12075a2-627c-462b-923f-c1a48a6a5b5e"))


class CASE_PRIORITY:
    MEDIUM = str(uuid.UUID("9d693ea9-53f2-42e1-a504-a51f212885cd"))
    HIGH = str(uuid.UUID("35d58f7a-df25-49af-9bf6-e19c4c82f702"))
    URGENT = str(uuid.UUID("0e7dc5aa-5278-45f9-94da-4c1a9b74a359"))
    LOW = str(uuid.UUID("565425ec-1996-41b9-8219-509ed2a2c959"))


class CASE_STATUS:
    ACTIVE = str(uuid.UUID("207ee23e-7be5-44cd-b8fb-6d2b692abd49"))
    PENDING = str(uuid.UUID("c6787af9-1828-479c-b377-16f51fe614fe"))
    STAYED = str(uuid.UUID("a1248c75-f5a2-4e63-869a-78dda51f6f86"))
    RESERVED = str(uuid.UUID("d11c4e3c-5c62-4d9c-a626-c589eb00ad7c"))
    DISPOSED = str(uuid.UUID("fb6bb7b4-7be6-4e19-b575-87cf1d92bf41"))


class CASE_ROLE:
    PETITIONER = str(uuid.UUID("348dbc26-9224-4755-948f-ed23f2ec0be2"))
    RESPONDENT = str(uuid.UUID("d2a27e68-938e-4b5c-8a85-f5c44a439e4e"))
    PLAINTIFF = str(uuid.UUID("805c852f-1107-4990-9cf1-9e9b9840a2cc"))
    DEFENDENT = str(uuid.UUID("2b956b74-937f-42bc-87d5-6d988fab6bd0"))
    APPLICANT = str(uuid.UUID("5c81c88e-b3ac-4bf0-8230-081369a3ba65"))
    COMPLAINANT = str(uuid.UUID("95fc8cef-f07c-45f0-9367-83590a056e8b"))
    ACCUSED = str(uuid.UUID("fa5e4a10-65a6-4c77-9b0b-dbb4254b4451"))
    APPELLANT = str(uuid.UUID("5634d0e8-e231-41d2-ad21-b828da3b7bbc"))
    OPPOSITE_PARTY = str(uuid.UUID("344bbdfd-96d7-45cd-9627-9d4916eefec9"))


class CASE_DOCUMENT_TYPE:
    PLAINT = str(uuid.UUID("6dba6809-b37b-42e2-8989-72f0f908e7f4"))
    WRITTEN_STATEMENT = str(uuid.UUID("a4b5e060-8f1f-453e-8e94-9d16b4758886"))
    APPLICATION = str(uuid.UUID("66eba10c-841c-4b33-939d-fe8885e24421"))
    ORDER = str(uuid.UUID("629e148e-c3fd-4dd2-b965-bf4a3b3aa895"))
    JUDGMENT = str(uuid.UUID("f3df1562-3cd4-43fc-859d-b10877134c8e"))
    AFFIDAVIT = str(uuid.UUID("deec8f34-561c-403c-96f3-6e1b8ca63389"))
    VAKALATNAMA = str(uuid.UUID("3c2da40f-b045-4646-b26d-b4281470da55"))
    OTHER = str(uuid.UUID("ad1b65a1-a10b-4cb5-8ca4-5af84a77bbae"))


class CASE_NOTE_TYPE:
    GENERAL_NOTE = str(uuid.UUID("105cadef-4a25-4c72-a18a-1de03a34ec6c"))
    COURT_ORDER = str(uuid.UUID("caca4acb-eb95-4e68-b2ae-74bfaed842c4"))
    CLIENT_COMMUNICATION = str(uuid.UUID("e7d9bc31-b651-4cad-8e93-7cf8f47f9982"))
    STRATEGY = str(uuid.UUID("22276614-4934-42ee-ab3b-d46ab183b7ae"))
    COURT_PROCEEDING = str(uuid.UUID("44189eaa-2bc3-46a6-9220-c83a7bc9946c"))


class BILLING_STATUS:
    PAID = str(uuid.UUID("6bbe1da5-e151-4dfd-9b85-2c62e6bb56d5"))
    UNPAID = str(uuid.UUID("42c09954-e7b1-46bb-941c-d6587b6e3ef6"))
    PARTIAL = str(uuid.UUID("d845cb2f-60e9-4108-88cc-fc40da54bb75"))

class CASE_DIARY_TYPE:
    HEARING = str(uuid.UUID("d6878c84-8d1e-4a74-8921-5940133ebb06"))
    EVIDENCE = str(uuid.UUID("4228fbda-4e71-4059-a60e-0f2b7c80217c"))
    ARGUMENTS = str(uuid.UUID("13f48b29-b48f-4497-8172-120f47d93152"))
    JUDGEMENT = str(uuid.UUID("5b9dfcc7-a9ec-4596-9add-ba66ab1c9185"))
    ORDER = str(uuid.UUID("2930e343-be87-4701-becc-94c43adba95c"))
    FILING_DEADLINE = str(uuid.UUID("5c9a178f-d647-417b-86ab-6faa8eed01b9"))
    LIMITATION_ALERT = str(uuid.UUID("59eb5d2a-b168-4501-88ee-688a69ac8d0f"))
    ADJOURNMENT = str(uuid.UUID("3248b217-0d47-48fe-9ba8-0727e9d54ad4"))
    MEETING = str(uuid.UUID("07e0bfc4-0f3e-412f-ae7a-bcd3dbe5e06e"))