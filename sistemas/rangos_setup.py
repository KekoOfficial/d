    # ── PASO 3: Eliminar TODO lo que NO está en config ──
    Logger.info("🔍 Eliminando rangos que no están en la configuración...")
    for nombre, rol in existentes.items():
        # No eliminar rangos que estén arriba del bot ni el propio rol del bot
        if rol.position >= guild.me.top_role.position:
            continue
        # Eliminar cualquier rango que no esté en la jerarquía
        if nombre not in jerarquia:
            try:
                await rol.delete()
                Logger.exito(f"🗑️ Eliminado rango: {nombre}")
                eliminados += 1
            except Exception as e:
                Logger.info(f"⚠️ No se pudo eliminar {nombre}: {e}")
