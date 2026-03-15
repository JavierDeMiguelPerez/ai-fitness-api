# views/workouts.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("🏋️‍♂️ Área de Entrenamientos")

# Validación de perfil
user_res = requests.get(f"{API_URL}/users/me", headers=headers)
if user_res.status_code != 200:
    st.warning("⚠️ Ve a la pestaña 'Mi Perfil' y completa tus datos antes de usar la IA.")
    st.stop()
user_data = user_res.json()

tab_gen, tab_saved, tab_log, tab_hist = st.tabs([
    "✨ Generar & Modificar", "📚 Mis Rutinas Guardadas", "📝 Tracking en Vivo", "📅 Historial & Edición"
])

# --- PESTAÑA 1: GENERAR Y MODIFICAR (IA) ---
with tab_gen:
    st.subheader("Diseñador de Rutinas IA")
    col1, col2 = st.columns([3, 1])
    with col1:
        goal = st.selectbox("Objetivo específico para esta rutina:", ["Hipertrophy", "Strength", "Weight Loss", "Endurance"])
    with col2:
        st.write("")
        st.write("")
        if st.button("🪄 Generar Nueva", type="primary", use_container_width=True):
            with st.spinner("Llama 3.1 calculando biomecánica..."):
                payload = {k: user_data.get(k) for k in ["age", "weight_kg", "height_cm", "gender", "experience_level"]}
                payload["primary_goal"] = goal
                res = requests.post(f"{API_URL}/workouts/generate", json=payload, headers=headers)
                if res.status_code == 200:
                    st.session_state.workout_plan = res.json()

    if "workout_plan" in st.session_state and st.session_state.workout_plan:
        plan = st.session_state.workout_plan
        st.success(f"Rutina activa: **{plan['plan_name']}**")
        
        # EL ENDPOINT /workouts/modify en acción
        st.write("¿No te convence algún ejercicio? Pídele a la IA que lo cambie:")
        col_mod_text, col_mod_btn = st.columns([4, 1])
        with col_mod_text:
            mod_prompt = st.text_input("Ej: 'Quita las sentadillas que me duele la rodilla y pon prensa'", label_visibility="collapsed")
        with col_mod_btn:
            if st.button("Aplicar IA", use_container_width=True):
                if mod_prompt:
                    with st.spinner("Reescribiendo rutina..."):
                        mod_res = requests.post(f"{API_URL}/workouts/modify", json={"current_plan": plan, "modification_prompt": mod_prompt}, headers=headers)
                        if mod_res.status_code == 200:
                            st.session_state.workout_plan = mod_res.json()
                            st.rerun()

        if st.button("💾 Guardar en Mis Rutinas", use_container_width=True):
            save_res = requests.post(f"{API_URL}/workouts/save", json={"plan": plan}, headers=headers)
            if save_res.status_code == 200:
                st.balloons()
                st.success("¡Rutina guardada en tu perfil de forma permanente!")

        for day in plan["days"]:
            with st.expander(f"📅 {day['day_name']}"):
                for ex in day["exercises"]:
                    st.write(f"- **{ex['name']}**: {ex['sets']} sets x {ex['reps']} reps ({ex['rest_seconds']}s desc.)")

# --- PESTAÑA 2: MIS RUTINAS (GET / DELETE) ---
with tab_saved:
    st.subheader("Tu Biblioteca de Rutinas")
    saved_res = requests.get(f"{API_URL}/workouts/saved", headers=headers)
    if saved_res.status_code == 200:
        for p in saved_res.json():
            with st.expander(f"⭐ {p['name']} ({p['created_at'][:10]})"):
                if st.button("🗑️ Borrar Rutina", key=f"del_plan_{p['id']}"):
                    requests.delete(f"{API_URL}/workouts/saved/{p['id']}", headers=headers)
                    st.rerun()
                for day in p['plan_data']['days']:
                    st.markdown(f"**{day['day_name']}**")
                    for ex in day['exercises']:
                        st.caption(f"- {ex['name']}: {ex['sets']}x{ex['reps']}")

# --- PESTAÑA 3: REGISTRO (POST /log) ---
with tab_log:
    st.subheader("Registra tu entrenamiento de hoy")
    day_name = st.text_input("Nombre de la sesión (ej. Día de Pecho / Martes)")
    
    if "log_table" not in st.session_state:
        st.session_state.log_table = [{"Ejercicio": "", "Serie": 1, "Reps": 0, "Peso (kg)": 0.0}]
    
    st.write("Añade tus series:")
    edited_data = st.data_editor(st.session_state.log_table, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 Guardar Sesión", type="primary"):
        if day_name and edited_data:
            exercises_dict = {}
            for row in edited_data:
                ex_name = row["Ejercicio"]
                if ex_name:
                    if ex_name not in exercises_dict: exercises_dict[ex_name] = []
                    exercises_dict[ex_name].append({"set_number": int(row["Serie"]), "reps": int(row["Reps"]), "weight_kg": float(row["Peso (kg)"])})
            
            payload_exercises = [{"exercise_name": name, "sets": sets} for name, sets in exercises_dict.items()]
            log_res = requests.post(f"{API_URL}/workouts/log", json={"day_name": day_name, "exercises": payload_exercises}, headers=headers)
            
            if log_res.status_code == 200:
                st.success("¡Entrenamiento registrado con éxito!")
                st.session_state.log_table = [{"Ejercicio": "", "Serie": 1, "Reps": 0, "Peso (kg)": 0.0}]

# --- PESTAÑA 4: HISTORIAL (GET, DELETE y EL NUEVO PUT /modify) ---
with tab_hist:
    st.subheader("Tu Historial de Entrenamientos")
    if "skip_w" not in st.session_state: st.session_state.skip_w = 0
    limit = 10
    
    hist_res = requests.get(f"{API_URL}/workouts/history?skip={st.session_state.skip_w}&limit={limit}", headers=headers)
    if hist_res.status_code == 200:
        history = hist_res.json()
        for session in history:
            with st.expander(f"📅 {session['date'][:10]} - {session['day_name']}"):
                c1, c2 = st.columns([1, 1])
                with c1:
                    if st.button("🗑️ Borrar", key=f"del_sess_{session['id']}"):
                        requests.delete(f"{API_URL}/workouts/history/{session['id']}", headers=headers)
                        st.rerun()
                
                st.write("**Editar esta sesión:**")
                # Preparamos los datos para el editor
                session_data = []
                for ex in session['exercises']:
                    for s in ex['sets']:
                        session_data.append({"Ejercicio": ex['exercise_name'], "Serie": s['set_number'], "Reps": s['reps'], "Peso (kg)": s['weight_kg']})
                
                # Editor independiente para cada sesión usando la key de Streamlit
                edited_session = st.data_editor(session_data, num_rows="dynamic", key=f"edit_sess_{session['id']}", use_container_width=True)
                
                if st.button("💾 Actualizar Sesión", key=f"upd_sess_{session['id']}"):
                    # Empaquetamos para el endpoint PUT
                    update_dict = {}
                    for row in edited_session:
                        ex_name = row["Ejercicio"]
                        if ex_name:
                            if ex_name not in update_dict: update_dict[ex_name] = []
                            update_dict[ex_name].append({"set_number": int(row["Serie"]), "reps": int(row["Reps"]), "weight_kg": float(row["Peso (kg)"])})
                    
                    update_payload = {"day_name": session['day_name'], "exercises": [{"exercise_name": name, "sets": sets} for name, sets in update_dict.items()]}
                    upd_res = requests.put(f"{API_URL}/workouts/history/{session['id']}", json=update_payload, headers=headers)
                    
                    if upd_res.status_code == 200:
                        st.success("Actualizado")
                        st.rerun()

        # Paginación visual
        st.write("---")
        cp1, cp2, cp3 = st.columns(3)
        with cp1:
            if st.button("⬅️ Recientes") and st.session_state.skip_w >= limit:
                st.session_state.skip_w -= limit
                st.rerun()
        with cp3:
            if len(history) == limit:
                if st.button("Antiguos ➡️"):
                    st.session_state.skip_w += limit
                    st.rerun()