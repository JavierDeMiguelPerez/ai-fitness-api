# views/workouts.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("🏋️‍♂️ Área de Entrenamientos")

# Obtenemos los datos del usuario para la generación
user_res = requests.get(f"{API_URL}/users/me", headers=headers)
if user_res.status_code != 200:
    st.warning("⚠️ Por favor, ve a la pestaña de 'Mi Perfil' y completa tus datos antes de usar la IA.")
    st.stop()
user_data = user_res.json()

tab_gen, tab_saved, tab_log, tab_hist = st.tabs([
    "✨ Generador IA", "📚 Mis Rutinas", "📝 Registrar Entreno", "📅 Historial"
])

# --- PESTAÑA 1: GENERAR Y MODIFICAR ---
with tab_gen:
    st.subheader("Diseña tu Plan Perfecto")
    col1, col2 = st.columns([3, 1])
    with col1:
        goal = st.selectbox("Objetivo hoy:", ["Hipertrophy", "Strength", "Weight Loss", "Endurance"])
    with col2:
        st.write("") # Espaciador
        st.write("")
        if st.button("Generar Nueva", type="primary", use_container_width=True):
            with st.spinner("Llama 3.1 calculando..."):
                payload = {k: user_data.get(k) for k in ["age", "weight_kg", "height_cm", "gender", "experience_level", "primary_goal"]}
                payload["primary_goal"] = goal
                res = requests.post(f"{API_URL}/workouts/generate", json=payload, headers=headers)
                if res.status_code == 200:
                    st.session_state.workout_plan = res.json()

    # Si hay una rutina generada en memoria, la mostramos y permitimos Modificar/Guardar
    if "workout_plan" in st.session_state and st.session_state.workout_plan:
        plan = st.session_state.workout_plan
        st.success(f"Rutina actual: **{plan['plan_name']}**")
        
        # Opciones de Guardar y Modificar
        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Guardar en Mis Rutinas", use_container_width=True):
                save_res = requests.post(f"{API_URL}/workouts/save", json={"plan": plan}, headers=headers)
                if save_res.status_code == 200:
                    st.balloons()
                    st.success("¡Guardada!")
        
        with c2:
            with st.popover("✏️ Modificar con IA", use_container_width=True):
                mod_prompt = st.text_input("¿Qué quieres cambiar?")
                if st.button("Aplicar Cambios"):
                    with st.spinner("Reescribiendo..."):
                        mod_res = requests.post(f"{API_URL}/workouts/modify", json={"current_plan": plan, "modification_prompt": mod_prompt}, headers=headers)
                        if mod_res.status_code == 200:
                            st.session_state.workout_plan = mod_res.json()
                            st.rerun()

        # Mostrar la rutina
        for day in plan["days"]:
            with st.expander(f"Día: {day['day_name']}"):
                for ex in day["exercises"]:
                    st.write(f"- **{ex['name']}**: {ex['sets']} sets x {ex['reps']} reps ({ex['rest_seconds']}s desc.)")

# --- PESTAÑA 2: MIS RUTINAS GUARDADAS (GET / DELETE) ---
with tab_saved:
    st.subheader("Tus Rutinas Favoritas")
    saved_res = requests.get(f"{API_URL}/workouts/saved", headers=headers)
    if saved_res.status_code == 200:
        saved_plans = saved_res.json()
        for p in saved_plans:
            with st.expander(f"⭐ {p['name']} ({p['created_at'][:10]})"):
                if st.button("🗑️ Borrar Rutina", key=f"del_plan_{p['id']}"):
                    requests.delete(f"{API_URL}/workouts/saved/{p['id']}", headers=headers)
                    st.rerun()
                for day in p['plan_data']['days']:
                    st.markdown(f"**{day['day_name']}**")
                    for ex in day['exercises']:
                        st.write(f"- {ex['name']}: {ex['sets']}x{ex['reps']}")

# --- PESTAÑA 3: REGISTRAR ENTRENO (Interactive Log) ---
with tab_log:
    st.subheader("Registra tus marcas de hoy")
    day_name = st.text_input("Nombre de la sesión (ej. Día de Pecho)")
    
    st.write("Anota tus ejercicios y series:")
    # Usamos st.data_editor para una tabla tipo Excel
    if "log_table" not in st.session_state:
        st.session_state.log_table = [{"Ejercicio": "Press Banca", "Serie": 1, "Reps": 10, "Peso (kg)": 60.0}]
    
    edited_data = st.data_editor(st.session_state.log_table, num_rows="dynamic", use_container_width=True)
    
    if st.button("💾 Guardar Sesión Finalizada", type="primary"):
        if day_name and edited_data:
            # Agrupamos la tabla en el JSON que espera la API
            exercises_dict = {}
            for row in edited_data:
                ex_name = row["Ejercicio"]
                if ex_name not in exercises_dict:
                    exercises_dict[ex_name] = []
                exercises_dict[ex_name].append({
                    "set_number": int(row["Serie"]),
                    "reps": int(row["Reps"]),
                    "weight_kg": float(row["Peso (kg)"])
                })
            
            payload_exercises = [{"exercise_name": name, "sets": sets} for name, sets in exercises_dict.items()]
            log_payload = {"day_name": day_name, "exercises": payload_exercises}
            
            log_res = requests.post(f"{API_URL}/workouts/log", json=log_payload, headers=headers)
            if log_res.status_code == 200:
                st.success("¡Entrenamiento registrado!")
                st.session_state.log_table = [{"Ejercicio": "", "Serie": 1, "Reps": 0, "Peso (kg)": 0.0}] # Reset

# --- PESTAÑA 4: HISTORIAL Y PAGINACIÓN ---
with tab_hist:
    st.subheader("Tu Progreso")
    # Paginación
    if "skip_w" not in st.session_state: st.session_state.skip_w = 0
    limit = 5
    
    hist_res = requests.get(f"{API_URL}/workouts/history?skip={st.session_state.skip_w}&limit={limit}", headers=headers)
    if hist_res.status_code == 200:
        history = hist_res.json()
        for session in history:
            with st.expander(f"📅 {session['date'][:10]} - {session['day_name']}"):
                if st.button("🗑️ Borrar", key=f"del_sess_{session['id']}"):
                    requests.delete(f"{API_URL}/workouts/history/{session['id']}", headers=headers)
                    st.rerun()
                for ex in session['exercises']:
                    st.markdown(f"**{ex['exercise_name']}**")
                    for s in ex['sets']:
                        st.write(f"- Serie {s['set_number']}: {s['reps']} reps con {s['weight_kg']} kg")
        
        # Botones de paginación
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("⬅️ Anteriores") and st.session_state.skip_w >= limit:
                st.session_state.skip_w -= limit
                st.rerun()
        with c3:
            if len(history) == limit: # Solo mostramos "Siguientes" si la página actual está llena
                if st.button("Siguientes ➡️"):
                    st.session_state.skip_w += limit
                    st.rerun()