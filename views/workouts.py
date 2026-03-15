# views/workouts.py
import streamlit as st
import requests
from datetime import date

API_URL = "http://127.0.0.1:8000"
headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("Area de Entrenamientos")

# Validación de perfil
user_res = requests.get(f"{API_URL}/users/me", headers=headers)
if user_res.status_code != 200:
    st.warning("Completa tu perfil antes de usar esta seccion. Ve a la pestana 'Perfil'.")
    st.stop()
user_data = user_res.json()

tab_active, tab_gen, tab_saved = st.tabs(["Rutina Activa", "Generar Rutina", "Mis Rutinas"])

# --- PESTAÑA 1: RUTINA ACTIVA ---
with tab_active:
    st.subheader("Tu Rutina Activa")
    
    active_res = requests.get(f"{API_URL}/workouts/active", headers=headers)
    
    if active_res.status_code == 200:
        active_plan = active_res.json()
        st.markdown(f"**{active_plan['name']}** — Creada el {active_plan['created_at'][:10]}")
        
        # Obtener historial completo para filtrar por ejercicio
        all_history = []
        skip = 0
        while True:
            hist_res = requests.get(f"{API_URL}/workouts/history?skip={skip}&limit=100", headers=headers)
            if hist_res.status_code == 200:
                batch = hist_res.json()
                if not batch:
                    break
                all_history.extend(batch)
                if len(batch) < 100:
                    break
                skip += 100
            else:
                break
        
        plan_data = active_plan["plan_data"]
        for day in plan_data["days"]:
            with st.expander(f"{day['day_name']}"):
                for ex in day["exercises"]:
                    ex_name = ex["name"]
                    st.markdown(f"**{ex_name}** — {ex['sets']} series x {ex['reps']} reps ({ex['rest_seconds']}s descanso)")
                    
                    # Historial de este ejercicio (con datos de sesión para edición)
                    ex_history = []
                    ex_sessions = {}  # session_id -> session data for PUT updates
                    for session in all_history:
                        for logged_ex in session["exercises"]:
                            if logged_ex["exercise_name"].lower().strip() == ex_name.lower().strip():
                                if session["id"] not in ex_sessions:
                                    ex_sessions[session["id"]] = session
                                for s in logged_ex["sets"]:
                                    ex_history.append({
                                        "session_id": session["id"],
                                        "Fecha": session["date"][:10],
                                        "Reps": s["reps"],
                                        "Peso (kg)": s["weight_kg"]
                                    })
                    
                    if ex_history:
                        st.caption("Historial de series anteriores (editable):")
                        edited_history = st.data_editor(
                            ex_history, 
                            use_container_width=True, 
                            hide_index=True,
                            disabled=["session_id", "Fecha"],
                            column_config={"session_id": None},
                            key=f"hist_{day['day_name']}_{ex_name}"
                        )
                        
                        # Detectar cambios y guardar
                        if edited_history != ex_history:
                            if st.button("Guardar cambios", key=f"save_hist_{day['day_name']}_{ex_name}"):
                                # Agrupar cambios por session_id
                                changed_sessions = set()
                                for i, row in enumerate(edited_history):
                                    if row != ex_history[i]:
                                        changed_sessions.add(row["session_id"])
                                
                                for sid in changed_sessions:
                                    session = ex_sessions[sid]
                                    # Reconstruir los ejercicios de la sesión con los valores editados
                                    updated_exercises = []
                                    for orig_ex in session["exercises"]:
                                        updated_sets = []
                                        set_counter = 1
                                        if orig_ex["exercise_name"].lower().strip() == ex_name.lower().strip():
                                            # Usar valores editados
                                            for row in edited_history:
                                                if row["session_id"] == sid:
                                                    updated_sets.append({
                                                        "set_number": set_counter,
                                                        "reps": int(row["Reps"]),
                                                        "weight_kg": float(row["Peso (kg)"])
                                                    })
                                                    set_counter += 1
                                        else:
                                            # Mantener ejercicios sin cambios
                                            for s in orig_ex["sets"]:
                                                updated_sets.append({
                                                    "set_number": s["set_number"],
                                                    "reps": s["reps"],
                                                    "weight_kg": s["weight_kg"]
                                                })
                                        updated_exercises.append({
                                            "exercise_name": orig_ex["exercise_name"],
                                            "sets": updated_sets
                                        })
                                    
                                    update_payload = {
                                        "day_name": session["day_name"],
                                        "exercises": updated_exercises
                                    }
                                    requests.put(f"{API_URL}/workouts/history/{sid}", json=update_payload, headers=headers)
                                
                                st.success("Historial actualizado correctamente.")
                                st.rerun()
                    else:
                        st.caption("Sin registros previos para este ejercicio.")
                    
                    # Formulario para registrar nueva serie (sin número de serie)
                    with st.form(key=f"add_set_{day['day_name']}_{ex_name}"):
                        st.write("Registrar nueva serie:")
                        col1, col2 = st.columns(2)
                        with col1:
                            new_reps = st.number_input("Reps", min_value=1, value=10, key=f"rp_{day['day_name']}_{ex_name}")
                        with col2:
                            new_weight = st.number_input("Peso (kg)", min_value=0.0, value=0.0, step=0.5, key=f"wt_{day['day_name']}_{ex_name}")
                        
                        # Auto-calcular número de serie
                        next_set_num = len([h for h in ex_history if h["Fecha"] == str(date.today())]) + 1
                        
                        add_submitted = st.form_submit_button("Guardar Serie")
                        if add_submitted:
                            payload = {
                                "day_name": day["day_name"],
                                "exercises": [{
                                    "exercise_name": ex_name,
                                    "sets": [{"set_number": next_set_num, "reps": new_reps, "weight_kg": new_weight}]
                                }]
                            }
                            log_res = requests.post(f"{API_URL}/workouts/log", json=payload, headers=headers)
                            if log_res.status_code == 200:
                                st.success("Serie registrada correctamente.")
                                st.rerun()
                            else:
                                st.error("Error al registrar la serie.")
                    
                    st.divider()
    
    else:
        # No hay rutina activa — mostrar las guardadas para elegir
        st.info("No tienes ninguna rutina activa seleccionada.")
        saved_res = requests.get(f"{API_URL}/workouts/saved", headers=headers)
        
        if saved_res.status_code == 200 and saved_res.json():
            saved_plans = saved_res.json()
            st.write("Selecciona una rutina para activarla:")
            
            for p in saved_plans:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{p['name']}** — {p['created_at'][:10]}")
                with col2:
                    if st.button("Activar", key=f"activate_from_active_{p['id']}"):
                        requests.put(f"{API_URL}/workouts/saved/{p['id']}/activate", headers=headers)
                        st.rerun()
        else:
            st.write("No tienes rutinas guardadas.")
            st.write("Genera una nueva rutina con la IA en la pestana 'Generar Rutina'.")


# --- PESTAÑA 2: GENERAR RUTINA ---
with tab_gen:
    st.subheader("Generador de Rutinas con IA")
    col1, col2 = st.columns([3, 1])
    with col1:
        goal = st.selectbox("Objetivo:", ["Hipertrofia", "Fuerza", "Perdida de grasa", "Resistencia"])
    with col2:
        st.write("")
        st.write("")
        if st.button("Generar Nueva", type="primary", use_container_width=True):
            with st.spinner("Generando rutina personalizada..."):
                goal_map = {"Hipertrofia": "Hipertrophy", "Fuerza": "Strength", "Perdida de grasa": "Weight Loss", "Resistencia": "Endurance"}
                payload = {k: user_data.get(k) for k in ["age", "weight_kg", "height_cm", "gender", "experience_level"]}
                payload["primary_goal"] = goal_map.get(goal, goal)
                res = requests.post(f"{API_URL}/workouts/generate", json=payload, headers=headers)
                if res.status_code == 200:
                    st.session_state.workout_plan = res.json()

    if "workout_plan" in st.session_state and st.session_state.workout_plan:
        plan = st.session_state.workout_plan
        st.success(f"Rutina generada: **{plan['plan_name']}**")
        
        st.write("Modifica la rutina con lenguaje natural:")
        col_mod_text, col_mod_btn = st.columns([4, 1])
        with col_mod_text:
            mod_prompt = st.text_input("Ej: 'Sustituye las sentadillas por prensa de piernas'", label_visibility="collapsed")
        with col_mod_btn:
            if st.button("Modificar", use_container_width=True):
                if mod_prompt:
                    with st.spinner("Modificando rutina..."):
                        mod_res = requests.post(f"{API_URL}/workouts/modify", json={"current_plan": plan, "modification_prompt": mod_prompt}, headers=headers)
                        if mod_res.status_code == 200:
                            st.session_state.workout_plan = mod_res.json()
                            st.rerun()

        if st.button("Guardar Rutina", use_container_width=True, type="primary"):
            save_res = requests.post(f"{API_URL}/workouts/save", json={"plan": plan}, headers=headers)
            if save_res.status_code == 200:
                st.success("Rutina guardada en tu biblioteca.")

        for day in plan["days"]:
            with st.expander(f"{day['day_name']}"):
                for ex in day["exercises"]:
                    st.write(f"- **{ex['name']}**: {ex['sets']} series x {ex['reps']} reps ({ex['rest_seconds']}s descanso)")


# --- PESTAÑA 3: MIS RUTINAS ---
with tab_saved:
    st.subheader("Tu Biblioteca de Rutinas")
    saved_res = requests.get(f"{API_URL}/workouts/saved", headers=headers)
    if saved_res.status_code == 200 and saved_res.json():
        for p in saved_res.json():
            with st.expander(f"{p['name']} ({p['created_at'][:10]})" + (" — ACTIVA" if p.get('is_active') else "")):
                col1, col2 = st.columns(2)
                with col1:
                    if not p.get("is_active"):
                        if st.button("Activar", key=f"activate_{p['id']}"):
                            requests.put(f"{API_URL}/workouts/saved/{p['id']}/activate", headers=headers)
                            st.rerun()
                    else:
                        st.caption("Esta es tu rutina activa")
                with col2:
                    if st.button("Borrar", key=f"del_plan_{p['id']}"):
                        requests.delete(f"{API_URL}/workouts/saved/{p['id']}", headers=headers)
                        st.rerun()
                
                for day in p["plan_data"]["days"]:
                    st.markdown(f"**{day['day_name']}**")
                    for ex in day["exercises"]:
                        st.caption(f"- {ex['name']}: {ex['sets']}x{ex['reps']}")
    else:
        st.info("No tienes rutinas guardadas. Genera una nueva en la pestana 'Generar Rutina'.")