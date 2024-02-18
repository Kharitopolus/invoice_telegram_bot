from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message

from admin.filters import admin_role
from services.manager import ManagerService

router: Router = Router()


@router.message(admin_role, Command(commands="list_managers"))
async def list_managers(message: Message):
    managers_id = await ManagerService().list_managers()

    return managers_id


@router.message(admin_role, Command(commands="add_manager"))
async def add_manager(message: Message, command: CommandObject):
    manager_id = int(command.args)

    await ManagerService().add_manager(manager_id)


@router.message(admin_role, Command(commands="delete_manager"))
async def delete_manager(message: Message, command: CommandObject):
    manager_id = int(command.args)

    await ManagerService().delete_manager(manager_id)
