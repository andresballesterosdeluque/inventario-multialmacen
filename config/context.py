def rol_usuario(request):
    """Pone el rol del usuario en todas las plantillas como {{ rol }}."""
    usuario = request.user
    if not usuario.is_authenticated:
        return {}
    if usuario.is_superuser:
        return {"rol": "Administrador"}
    grupo = usuario.groups.first()
    return {"rol": grupo.name if grupo else "Sin rol"}
