from app.schemas.user import UserBase


def map_message_variables(lead: UserBase):
    return {
            "1": lead.first_name,
            "2": lead.phone
        }
    