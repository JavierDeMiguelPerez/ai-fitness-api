# views/nutrition.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("Area de Nutricion")

tab_actual, tab_gen, tab_saved, tab_log, tab_hist = st.tabs([
    "Dieta Actual", "Generar Dieta", "Mis Dietas", "Registrar Comida", "Historial de Comidas"
])

# --- PESTAÑA 1: DIETA ACTUAL ---
with tab_actual:
    st.subheader("Tu Dieta Activa")
    
    active_res = requests.get(f"{API_URL}/diets/active", headers=headers)
    
    if active_res.status_code == 200:
        active_diet = active_res.json()
        st.markdown(f"**{active_diet['name']}** — Creada el {active_diet['created_at'][:10]}")
        
        plan_data = active_diet["plan_data"]
        for day in plan_data["days"]:
            with st.expander(f"{day['day_name']} — {day['total_calories']} kcal"):
                for meal in day["meals"]:
                    st.markdown(f"**{meal['meal_name']}**: {meal['description']}")
                    st.caption(f"{meal['calories']} kcal | Prot: {meal['protein_g']}g | Carb: {meal['carbs_g']}g | Grasas: {meal['fats_g']}g")
    else:
        st.info("No tienes ninguna dieta activa seleccionada.")
        saved_res = requests.get(f"{API_URL}/diets/saved", headers=headers)
        
        if saved_res.status_code == 200 and saved_res.json():
            saved_diets = saved_res.json()
            st.write("Selecciona una dieta para activarla:")
            
            for d in saved_diets:
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"**{d['name']}** — {d['created_at'][:10]}")
                with col2:
                    if st.button("Activar", key=f"activate_diet_from_actual_{d['id']}"):
                        requests.put(f"{API_URL}/diets/saved/{d['id']}/activate", headers=headers)
                        st.rerun()
        else:
            st.write("No tienes dietas guardadas.")
            st.write("Genera una nueva dieta con la IA en la pestana 'Generar Dieta'.")


# --- PESTAÑA 2: GENERAR DIETA ---
with tab_gen:
    st.subheader("Generador de Dietas con IA")
    if st.button("Generar Menu Semanal", type="primary"):
        with st.spinner("Calculando macros y generando menu..."):
            res = requests.post(f"{API_URL}/diets/generate", headers=headers)
            if res.status_code == 200:
                st.session_state.diet_plan = res.json()

    if "diet_plan" in st.session_state and st.session_state.diet_plan:
        plan = st.session_state.diet_plan
        st.success(f"Dieta generada: **{plan['plan_name']}**")
        
        st.write("Modifica la dieta con lenguaje natural:")
        col_mod_text, col_mod_btn = st.columns([4, 1])
        with col_mod_text:
            mod_prompt_diet = st.text_input("Ej: 'Soy intolerante a la lactosa, cambia los lacteos'", label_visibility="collapsed")
        with col_mod_btn:
            if st.button("Modificar", use_container_width=True, key="mod_diet_btn"):
                if mod_prompt_diet:
                    with st.spinner("Modificando dieta..."):
                        mod_res = requests.post(f"{API_URL}/diets/modify", json={"current_plan": plan, "modification_prompt": mod_prompt_diet}, headers=headers)
                        if mod_res.status_code == 200:
                            st.session_state.diet_plan = mod_res.json()
                            st.rerun()

        if st.button("Guardar Dieta", use_container_width=True, type="primary"):
            save_res = requests.post(f"{API_URL}/diets/save", json={"plan": plan}, headers=headers)
            if save_res.status_code == 200:
                st.success("Dieta guardada en tu biblioteca.")

        for day in plan["days"]:
            with st.expander(f"{day['day_name']} — {day['total_calories']} kcal"):
                for meal in day["meals"]:
                    st.markdown(f"**{meal['meal_name']}**: {meal['description']}")
                    st.caption(f"{meal['calories']} kcal | Prot: {meal['protein_g']}g | Carb: {meal['carbs_g']}g | Grasas: {meal['fats_g']}g")


# --- PESTAÑA 3: MIS DIETAS ---
with tab_saved:
    st.subheader("Tu Biblioteca de Dietas")
    saved_res = requests.get(f"{API_URL}/diets/saved", headers=headers)
    if saved_res.status_code == 200 and saved_res.json():
        for d in saved_res.json():
            with st.expander(f"{d['name']} ({d['created_at'][:10]})" + (" — ACTIVA" if d.get('is_active') else "")):
                col1, col2 = st.columns(2)
                with col1:
                    if not d.get("is_active"):
                        if st.button("Activar", key=f"activate_diet_{d['id']}"):
                            requests.put(f"{API_URL}/diets/saved/{d['id']}/activate", headers=headers)
                            st.rerun()
                    else:
                        st.caption("Esta es tu dieta activa")
                with col2:
                    if st.button("Borrar", key=f"del_diet_{d['id']}"):
                        requests.delete(f"{API_URL}/diets/saved/{d['id']}", headers=headers)
                        st.rerun()
                
                for day in d["plan_data"]["days"]:
                    st.write(f"**{day['day_name']}** — {day['total_calories']} kcal")
    else:
        st.info("No tienes dietas guardadas. Genera una nueva en la pestana 'Generar Dieta'.")


# --- PESTAÑA 4: REGISTRAR COMIDA ---
with tab_log:
    st.subheader("Registro de Comidas por Lenguaje Natural")
    st.write("Escribe lo que has comido y la IA calculara los macros automaticamente.")
    
    meal_text = st.text_area("¿Que has comido?", placeholder="Ej: Un plato de arroz con pollo y ensalada")
    
    if st.button("Calcular y Guardar", type="primary"):
        if meal_text:
            with st.spinner("Analizando alimentos..."):
                log_res = requests.post(f"{API_URL}/diets/log", json={"meal_text": meal_text}, headers=headers)
                if log_res.status_code == 200:
                    m = log_res.json()
                    st.success("Comida registrada correctamente.")
                    st.info(f"**Alimento detectado:** {m['food_recognized']}")
                    
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Calorias", f"{m['calories']} kcal")
                    c2.metric("Proteinas", f"{m['protein_g']} g")
                    c3.metric("Carbohidratos", f"{m['carbs_g']} g")
                    c4.metric("Grasas", f"{m['fats_g']} g")
                else:
                    st.error("Error al analizar la comida.")


# --- PESTAÑA 5: HISTORIAL DE COMIDAS ---
with tab_hist:
    st.subheader("Historial de Comidas")
    if "skip_d" not in st.session_state:
        st.session_state.skip_d = 0
    limit_d = 10
    
    hist_res = requests.get(f"{API_URL}/diets/history?skip={st.session_state.skip_d}&limit={limit_d}", headers=headers)
    if hist_res.status_code == 200:
        meals = hist_res.json()
        if meals:
            for meal in meals:
                with st.container(border=True):
                    c1, c2 = st.columns([9, 1])
                    c1.markdown(f"**{meal['food_recognized']}**")
                    c1.caption(f"{meal['logged_at'][:16]} | {meal['calories']} kcal | Prot: {meal['protein_g']}g | Carb: {meal['carbs_g']}g | Grasas: {meal['fats_g']}g")
                    if c2.button("Borrar", key=f"del_log_{meal['id']}"):
                        requests.delete(f"{API_URL}/diets/history/{meal['id']}", headers=headers)
                        st.rerun()
            
            st.divider()
            cp1, cp2, cp3 = st.columns(3)
            with cp1:
                if st.session_state.skip_d >= limit_d:
                    if st.button("Recientes", key="prev_d"):
                        st.session_state.skip_d -= limit_d
                        st.rerun()
            with cp3:
                if len(meals) == limit_d:
                    if st.button("Anteriores", key="next_d"):
                        st.session_state.skip_d += limit_d
                        st.rerun()
        else:
            st.info("No hay registros de comidas.")