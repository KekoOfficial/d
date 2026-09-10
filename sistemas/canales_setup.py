        # ── Cada juego con su propio chat ──
        if "subcanales" in cat_data:
            for juego_nombre, juego_data in cat_data["subcanales"].items():
                requiere = juego_data.get("requiere_rango")
                permisos_juego = obtener_permisos_base(guild, ver=False, hablar=False, requiere_rango=requiere)
                
                # Crea cada canal de texto y voz para este juego
                for canal_info in juego_data.get("canales", []):
                    nombre_canal = canal_info["nombre"]
                    tipo = canal_info["tipo"]
                    
                    if nombre_canal not in existentes_nombres:
                        if tipo == "text":
                            await guild.create_text_channel(
                                name=nombre_canal,
                                category=categoria,
                                overwrites=permisos_juego
                            )
                        elif tipo == "voice":
                            await guild.create_voice_channel(
                                name=nombre_canal,
                                category=categoria,
                                overwrites=permisos_juego
                            )
                        registrar_canal_creado(nombre_canal)
                        Logger.exito(f"  ✅ {nombre_canal}")
                        creados += 1
                    else:
                        Logger.info(f"  ⏭️ {nombre_canal} — ya existe")
