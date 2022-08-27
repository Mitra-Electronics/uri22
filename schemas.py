from pydantic import AnyUrl, BaseModel, EmailStr, NonNegativeInt


class Accounts(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    referrals_created: NonNegativeInt


class Login(BaseModel):
    email: EmailStr
    password: str


class AccInput(Login):
    first_name: str
    last_name: str


class URLInput(BaseModel):
    url: AnyUrl
    payment_required: bool = False


class URLEdit(BaseModel):
    url: AnyUrl
    referral_id: str


class URLDelete(BaseModel):
    referral_id: str


class URL(URLInput):
    referral_id: str
    account_id: str
    is_active: bool
    referrals: int
