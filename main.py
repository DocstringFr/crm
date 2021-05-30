import typer
from api.crm import User, get_all_users

app = typer.Typer()


@app.command()
def add(first_name: str = typer.Argument(..., help="Prénom"),
        last_name: str = typer.Argument(..., help="Nom de famille"),
        address: str = typer.Argument(None, help="Adresse"),
        phone_number: str = typer.Argument(None, help="Numéro de téléphone")):
    """Ajouter un contact"""

    user = User(first_name=first_name,
                last_name=last_name,
                address=address,
                phone_number=phone_number)
    user_id = user.save()
    if user_id == -1:
        typer.secho(f"Le contact {user.full_name} existe déjà.", fg=typer.colors.RED)
    else:
        typer.echo(f"Contact {user.full_name} ajouté.")


@app.command("list")
def list_users():
    """Afficher tous les contacts"""
    for user in get_all_users():
        typer.secho(user.full_name, bg=typer.colors.BLUE, fg=typer.colors.BRIGHT_WHITE, bold=True)
        typer.echo(user.address if user.address else "Aucune adresse.")
        typer.echo(user.phone_number if user.phone_number else "Aucun numéro.")

        typer.echo("-" * 20)


@app.command()
def delete(first_name: str, last_name: str):
    """Supprimer un contact"""

    user = User(first_name, last_name)
    contact = typer.style(user.full_name, bg=typer.colors.BLUE, fg=typer.colors.BRIGHT_WHITE)
    if user.exists():
        user.delete()
        typer.echo(f"Contact {contact} supprimé.")
    else:
        typer.echo(f"Le contact {contact} n'existe pas.")


@app.command()
def clear():
    """Supprimer tous les contacts"""

    typer.confirm("Voulez-vous supprimer tous vos contacts ?", abort=True)

    users = get_all_users()
    for user in users:
        user.delete()
        typer.secho(f"Suppression de {user.full_name}.", fg=typer.colors.RED)


if __name__ == '__main__':
    app()
