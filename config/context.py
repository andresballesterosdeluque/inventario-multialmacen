def rol_usuario(request):
    """Pone el rol del usuario en todas las plantillas como {{ rol }}."""
    usuario = request.user
    if not usuario.is_authenticated:
        return {}
    return {"rol": usuario.get_usu_rol_display()}
