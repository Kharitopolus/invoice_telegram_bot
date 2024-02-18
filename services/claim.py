from client.schemas import ClaimSchema
from database import async_session_maker
from repositories.repositories import ClaimRepository
from services.invoice import InvoiceService
from unitofwork import UnitOfWork
from utils import model_to_text


class ClaimService:

    def __init__(self):
        self.uow = UnitOfWork(
            async_session_maker,
            [
                ClaimRepository,
            ],
        )

    async def add_claim(self, invoice: ClaimSchema):
        data = invoice.model_dump(exclude_unset=True)

        async with self.uow:
            claim = await self.uow.claim.add_one(data)
            await self.uow.commit()

        return claim

    async def list_claims_for_client(self, client_id: int):
        async with self.uow:
            condition = {'client_id': client_id}
            claim_models = await self.uow.claim.find_with_condition(condition)
            claim_schemas = [
                ClaimSchema.model_validate(claim_model)
                for claim_model in claim_models
            ]
            return claim_schemas

    async def claim_to_text(self, claim_id: int, with_image: bool = False):
        async with self.uow:
            claim = await self.uow.claim.get_one(claim_id)
            attributes_aliases = {
                'description': 'описание претензии',
                'contact_email': 'контактная почта',
            }
            claim_text = model_to_text(
                claim,
                attributes_aliases,
            )
            invoice_text = await InvoiceService().invoice_to_text(claim.invoice_id)

            if with_image:
                return invoice_text + claim_text, claim.image_name
            else:
                return invoice_text + claim_text

