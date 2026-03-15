# views/nutrition.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("🥗 Área de Nutrición")

tab_gen, tab_saved, tab_nlp, tab_hist = st.tabs([
    "✨ Diseñar Dieta IA", "📚 Mis Dietas Guardadas", "🍎 Registro Inteligente (NLP)", "📅 Historial"
])

# --- PESTAÑA 1: GENERAR Y MODIFICAR (IA) ---
with tab_gen:
    st.subheader("Tu Chef Inteligente")
    if st.button("🪄 Generar Menú Semanal", type="primary"):
        with st.spinner("Calculando macros óptimos..."):
            res = requests.post(f"{API_URL}/diets/generate", headers=headers)
            if res.status_code == 200:
                st.session_state.diet_plan = res.json()

    if "diet_plan" in st.session_state and st.session_state.diet_plan:
        plan = st.session_state.diet_plan
        st.success(f"Dieta activa: **{plan['plan_name']}**")
        
        # EL ENDPOINT /diets/modify
        st.write("¿Tienes alergias o no te gusta un alimento? Ajustémoslo:")
        col_mod_text, col_mod_btn = st.columns([4, 1])
        with col_mod_text:
            mod_prompt_diet = st.text_input("Ej: 'Soy intolerante a la lactosa, cambia los lácteos'", label_visibility="collapsed")
        with col_mod_btn:
            if st.button("Aplicar IA", use_container_width=True, key="mod_diet_btn"):
                if mod_prompt_diet:
                    with st.spinner("Adaptando el menú..."):
                        mod_res = requests.post(f"{API_URL}/diets/modify", json={"current_plan": plan, "modification_prompt": mod_prompt_diet}, headers=headers)
                        if mod_res.status_code == 200:
                            st.session_state.diet_plan = mod_res.json()
                            st.rerun()

        if st.button("💾 Guardar Dieta", use_container_width=True):
            save_res = requests.post(f"{API_URL}/diets/save", json={"plan": plan}, headers=headers)
            if save_res.status_code == 200:
                st.balloons()
                st.success("¡Menú guardado en tu biblioteca!")

        for day in plan["days"]:
            with st.expander(f"📅 {day['day_name']} - {day['total_calories']} kcal"):
                for meal in day["meals"]:
                    st.markdown(f"**{meal['meal_name']}**: {meal['description']}")
                    st.caption(f"🔥 {meal['calories']} kcal | 🥩 Prot: {meal['protein_g']}g | 🥖 Carb: {meal['carbs_g']}g | 🥑 Grasas: {meal['fats_g']}g")

# --- PESTAÑA 2: MIS DIETAS GUARDADAS (GET / DELETE) ---
with tab_saved:
    st.subheader("Tu Biblioteca Nutricional")
    saved_res = requests.get(f"{API_URL}/diets/saved", headers=headers)
    if saved_res.status_code == 200:
        for d in saved_res.json():
            with st.expander(f"⭐ {d['name']} ({d['created_at'][:10]})"):
                if st.button("🗑️ Borrar Dieta", key=f"del_diet_{d['id']}"):
                    requests.delete(f"{API_URL}/diets/saved/{d['id']}", headers=headers)
                    st.rerun()
                for day in d['plan_data']['days']:
                    st.write(f"**{day['day_name']}** - {day['total_calories']} kcal")

# --- PESTAÑA 3: TRACKING DE COMIDA NLP (POST /log) ---
with tab_nlp:
    st.subheader("Registro Inteligente de Comidas")
    st.write("Escribe lo que has comido en lenguaje natural. La IA hará las matemáticas por ti.")
    
    meal_text = st.text_area("¿Qué has comido hoy?", placeholder="Ej: Un plato de salmorejo con jamón y tortilla española")
    
    if st.button("Calcular y Guardar 🍎", type="primary"):
        if meal_text:
            with st.spinner("Analizando alimentos..."):
                log_res = requests.post(f"{API_URL}/diets/log", json={"meal_text": meal_text}, headers=headers)
                if log_res.status_code == 200:
                    m = log_res.json()
                    st.success("¡Guardado en el historial!")
                    st.info(f"**Comida detectada:** {m['food_recognized']}")
                    
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Calorías", f"{m['calories']} kcal")
                    c2.metric("Proteínas", f"{m['protein_g']} g")
                    c3.metric("Carbohidratos", f"{m['carbs_g']} g")
                    c4.metric("Grasas", f"{m['fats_g']} g")

# --- PESTAÑA 4: HISTORIAL PAGINADO (GET / DELETE) ---
with tab_hist:
    st.subheader("Tu Historial Diario")
    if "skip_d" not in st.session_state: st.session_state.skip_d = 0
    limit_d = 10
    
    hist_res = requests.get(f"{API_URL}/diets/history?skip={st.session_state.skip_d}&limit={limit_d}", headers=headers)
    if hist_res.status_code == 200:
        for meal in hist_res.json():
            with st.container(border=True):
                c1, c2 = st.columns([9, 1])
                c1.markdown(f"**{meal['food_recognized']}** \n*{meal['logged_at'][:16]}*")
                c1.caption(f"🔥 {meal['calories']} kcal | 🥩 {meal['protein_g']}g | 🥖 {meal['carbs_g']}g | 🥑 {meal['fats_g']}g")
                if c2.button("🗑️", key=f"del_log_{meal['id']}"):
                    requests.delete(f"{API_URL}/diets/history/{meal['id']}", headers=headers)
                    st.rerun()
                    
        # Paginación visual
        st.write("---")
        cp1, cp2, cp3 = st.columns(3)
        with cp1:
            if st.button("⬅️ Recientes", key="prev_d") and st.session_state.skip_d >= limit_d:
                st.session_state.skip_d -= limit_d
                st.rerun()
        with cp3:
            if len(hist_res.json()) == limit_d:
                if st.button("Antiguos ➡️", key="next_d"):
                    st.session_state.skip_d += limit_d
                    st.rerun()