--
-- PostgreSQL database dump
--

\restrict dGoSDuDhf3R7Dhk9r3scXo9RoNWPl5UpjwiRcIpUzbiiavU8AYZrhsoYm5TIFcJ

-- Dumped from database version 16.13
-- Dumped by pg_dump version 16.13

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: uuid-ossp; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;


--
-- Name: EXTENSION "uuid-ossp"; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION "uuid-ossp" IS 'generate universally unique identifiers (UUIDs)';


--
-- Name: update_updated_at_column(); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION public.update_updated_at_column() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: contactos_emergencia; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.contactos_emergencia (
    id integer NOT NULL,
    paciente_id integer NOT NULL,
    nombres_completos character varying(150) NOT NULL,
    telefono character varying(20) NOT NULL,
    parentesco character varying(50),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    activo boolean DEFAULT true,
    version integer DEFAULT 1
);


--
-- Name: contactos_emergencia_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.contactos_emergencia_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: contactos_emergencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.contactos_emergencia_id_seq OWNED BY public.contactos_emergencia.id;


--
-- Name: hce_antecedentes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hce_antecedentes (
    id integer NOT NULL,
    paciente_id integer NOT NULL,
    tipo character varying(50) NOT NULL,
    nombre character varying(150) NOT NULL,
    descripcion text,
    fecha_diagnostico date,
    activo boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    version integer DEFAULT 1,
    CONSTRAINT hce_antecedentes_tipo_check CHECK (((tipo)::text = ANY ((ARRAY['Alergia'::character varying, 'Patologia'::character varying, 'Cirugia'::character varying, 'Medicamento'::character varying])::text[])))
);


--
-- Name: hce_antecedentes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hce_antecedentes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hce_antecedentes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hce_antecedentes_id_seq OWNED BY public.hce_antecedentes.id;


--
-- Name: hce_consulta_previa; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.hce_consulta_previa (
    id integer NOT NULL,
    paciente_id integer NOT NULL,
    fecha_consulta timestamp without time zone NOT NULL,
    motivo text,
    diagnostico_medico text,
    tratamiento text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    version integer DEFAULT 1,
    activo boolean DEFAULT true
);


--
-- Name: hce_consulta_previa_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.hce_consulta_previa_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: hce_consulta_previa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.hce_consulta_previa_id_seq OWNED BY public.hce_consulta_previa.id;


--
-- Name: logs_auditoria; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.logs_auditoria (
    id integer NOT NULL,
    usuario_id integer,
    accion character varying(20) NOT NULL,
    modulo character varying(50) NOT NULL,
    registro_id integer NOT NULL,
    datos_anteriores jsonb,
    datos_nuevos jsonb,
    ip_address inet,
    user_agent text,
    "timestamp" timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT logs_auditoria_accion_check CHECK (((accion)::text = ANY ((ARRAY['INSERT'::character varying, 'UPDATE'::character varying, 'DELETE'::character varying, 'STATUS_CHANGE'::character varying])::text[])))
);


--
-- Name: logs_auditoria_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.logs_auditoria_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: logs_auditoria_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.logs_auditoria_id_seq OWNED BY public.logs_auditoria.id;


--
-- Name: pacientes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pacientes (
    id integer NOT NULL,
    dni character varying(20) NOT NULL,
    nombres character varying(100) NOT NULL,
    apellidos character varying(100) NOT NULL,
    fecha_nacimiento date NOT NULL,
    genero character varying(10),
    telefono character varying(20),
    email character varying(100),
    direccion text,
    activo boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    version integer DEFAULT 1,
    CONSTRAINT chk_fecha_nacimiento CHECK ((fecha_nacimiento <= CURRENT_DATE)),
    CONSTRAINT pacientes_genero_check CHECK (((genero)::text = ANY ((ARRAY['M'::character varying, 'F'::character varying, 'Otros'::character varying])::text[])))
);


--
-- Name: pacientes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pacientes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: pacientes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pacientes_id_seq OWNED BY public.pacientes.id;


--
-- Name: resultados_ia; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.resultados_ia (
    id integer NOT NULL,
    triaje_id integer NOT NULL,
    prompt_enviado text NOT NULL,
    respuesta_raw_llm text NOT NULL,
    diagnosticos_json jsonb,
    recomendaciones_json jsonb,
    modelo_utilizado character varying(50),
    latencia_segundos numeric(5,2),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    activo boolean DEFAULT true,
    version integer DEFAULT 1
);


--
-- Name: resultados_ia_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.resultados_ia_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: resultados_ia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.resultados_ia_id_seq OWNED BY public.resultados_ia.id;


--
-- Name: signos_vitales; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.signos_vitales (
    id integer NOT NULL,
    triaje_id integer NOT NULL,
    presion_sistolica integer,
    presion_diastolica integer,
    frecuencia_cardiaca integer,
    frecuencia_respiratoria integer,
    temperatura numeric(4,1),
    saturacion_o2 integer,
    nota_suplementaria text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    activo boolean DEFAULT true,
    version integer DEFAULT 1,
    CONSTRAINT signos_vitales_frecuencia_cardiaca_check CHECK (((frecuencia_cardiaca >= 30) AND (frecuencia_cardiaca <= 250))),
    CONSTRAINT signos_vitales_frecuencia_respiratoria_check CHECK (((frecuencia_respiratoria >= 5) AND (frecuencia_respiratoria <= 60))),
    CONSTRAINT signos_vitales_presion_diastolica_check CHECK (((presion_diastolica >= 30) AND (presion_diastolica <= 200))),
    CONSTRAINT signos_vitales_presion_sistolica_check CHECK (((presion_sistolica >= 50) AND (presion_sistolica <= 250))),
    CONSTRAINT signos_vitales_saturacion_o2_check CHECK (((saturacion_o2 >= 0) AND (saturacion_o2 <= 100))),
    CONSTRAINT signos_vitales_temperatura_check CHECK (((temperatura >= (30)::numeric) AND (temperatura <= (45)::numeric)))
);


--
-- Name: signos_vitales_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.signos_vitales_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: signos_vitales_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.signos_vitales_id_seq OWNED BY public.signos_vitales.id;


--
-- Name: sintomas_triaje; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.sintomas_triaje (
    id integer NOT NULL,
    triaje_id integer NOT NULL,
    sintoma character varying(100) NOT NULL,
    intensidad character varying(20),
    descripcion_libre text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    activo boolean DEFAULT true,
    version integer DEFAULT 1,
    CONSTRAINT sintomas_triaje_intensidad_check CHECK (((intensidad)::text = ANY ((ARRAY['Leve'::character varying, 'Moderado'::character varying, 'Grave'::character varying])::text[])))
);


--
-- Name: sintomas_triaje_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.sintomas_triaje_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: sintomas_triaje_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.sintomas_triaje_id_seq OWNED BY public.sintomas_triaje.id;


--
-- Name: triajes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.triajes (
    id integer NOT NULL,
    paciente_id integer NOT NULL,
    usuario_id integer NOT NULL,
    fecha_hora timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    motivo_consulta text NOT NULL,
    nivel_urgencia_asignado_ia character varying(10),
    nivel_urgencia_final character varying(10),
    estado_logistico character varying(20) DEFAULT 'En Espera'::character varying,
    notas_medicas text,
    diagnostico_final_medico text,
    tiempo_atencion_segundos integer,
    activo boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    version integer DEFAULT 1,
    sincronizado_hce boolean DEFAULT false NOT NULL,
    fecha_sincronizacion_hce timestamp without time zone,
    hce_sync boolean DEFAULT false,
    hce_sync_at timestamp without time zone,
    CONSTRAINT triajes_estado_logistico_check CHECK (((estado_logistico)::text = ANY ((ARRAY['En Espera'::character varying, 'Llamado'::character varying, 'En Atencion'::character varying, 'Atendido'::character varying])::text[]))),
    CONSTRAINT triajes_nivel_urgencia_asignado_ia_check CHECK (((nivel_urgencia_asignado_ia)::text = ANY ((ARRAY['RED'::character varying, 'ORANGE'::character varying, 'YELLOW'::character varying, 'GREEN'::character varying, 'BLUE'::character varying])::text[]))),
    CONSTRAINT triajes_nivel_urgencia_final_check CHECK (((nivel_urgencia_final)::text = ANY ((ARRAY['RED'::character varying, 'ORANGE'::character varying, 'YELLOW'::character varying, 'GREEN'::character varying, 'BLUE'::character varying])::text[])))
);


--
-- Name: triajes_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.triajes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: triajes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.triajes_id_seq OWNED BY public.triajes.id;


--
-- Name: usuarios; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.usuarios (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    hashed_password character varying(255) NOT NULL,
    nombres character varying(100),
    apellidos character varying(100),
    rol character varying(20) NOT NULL,
    activo boolean DEFAULT true,
    last_login timestamp without time zone,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    version integer DEFAULT 1,
    CONSTRAINT usuarios_rol_check CHECK (((rol)::text = ANY ((ARRAY['enfermera'::character varying, 'medico'::character varying, 'gerente'::character varying, 'auditor'::character varying])::text[])))
);


--
-- Name: usuarios_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.usuarios_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: usuarios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.usuarios_id_seq OWNED BY public.usuarios.id;


--
-- Name: contactos_emergencia id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contactos_emergencia ALTER COLUMN id SET DEFAULT nextval('public.contactos_emergencia_id_seq'::regclass);


--
-- Name: hce_antecedentes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hce_antecedentes ALTER COLUMN id SET DEFAULT nextval('public.hce_antecedentes_id_seq'::regclass);


--
-- Name: hce_consulta_previa id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hce_consulta_previa ALTER COLUMN id SET DEFAULT nextval('public.hce_consulta_previa_id_seq'::regclass);


--
-- Name: logs_auditoria id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.logs_auditoria ALTER COLUMN id SET DEFAULT nextval('public.logs_auditoria_id_seq'::regclass);


--
-- Name: pacientes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes ALTER COLUMN id SET DEFAULT nextval('public.pacientes_id_seq'::regclass);


--
-- Name: resultados_ia id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resultados_ia ALTER COLUMN id SET DEFAULT nextval('public.resultados_ia_id_seq'::regclass);


--
-- Name: signos_vitales id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos_vitales ALTER COLUMN id SET DEFAULT nextval('public.signos_vitales_id_seq'::regclass);


--
-- Name: sintomas_triaje id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sintomas_triaje ALTER COLUMN id SET DEFAULT nextval('public.sintomas_triaje_id_seq'::regclass);


--
-- Name: triajes id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.triajes ALTER COLUMN id SET DEFAULT nextval('public.triajes_id_seq'::regclass);


--
-- Name: usuarios id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios ALTER COLUMN id SET DEFAULT nextval('public.usuarios_id_seq'::regclass);


--
-- Data for Name: contactos_emergencia; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.contactos_emergencia (id, paciente_id, nombres_completos, telefono, parentesco, created_at, updated_at, activo, version) FROM stdin;
1	1	Maria Martinez	555-0201	Esposa	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
2	2	Jose Lopez	555-0202	Padre	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
3	3	Carmen Garcia	555-0203	Esposa	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
4	4	Roberto Rodriguez	555-0204	Padre	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
5	5	Diana Sanchez	555-0205	Esposa	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
6	6	Luis Perez	555-0206	Hermano	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
7	7	Elena Fernandez	555-0207	Esposa	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
8	8	Miguel Gonzalez	555-0208	Padre	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
9	9	Ana Ramirez	555-0209	Esposa	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
10	10	Juan Torres	555-0210	Padre	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
11	11	Sofia Vargas	555-0211	Esposa	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
12	12	Carlos Castro	555-0212	Hermano	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
13	13	Patricia Morales	555-0213	Esposa	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
14	14	Diego Ortega	555-0214	Padre	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
15	15	Gabriela Herrera	555-0215	Esposa	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
16	16	Fernando Silva	555-0216	Hermano	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
17	17	Laura Mendoza	555-0217	Esposa	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
18	18	Santiago Rojas	555-0218	Padre	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
19	19	Isabel Guerrero	555-0219	Esposa	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
20	20	Emilio Cruz	555-0220	Padre	2026-05-03 00:02:55.353628	2026-05-03 00:02:55.353628	t	1
\.


--
-- Data for Name: hce_antecedentes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hce_antecedentes (id, paciente_id, tipo, nombre, descripcion, fecha_diagnostico, activo, created_at, updated_at, version) FROM stdin;
1	1	Patologia	Hipertension arterial	HTA diagnosticada hace 5 aÃ±os	2019-03-15	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
2	1	Medicamento	Losartan	50mg diario	2019-03-15	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
3	1	Alergia	Penicilina	Urticaria	2010-06-20	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
4	3	Patologia	Diabetes mellitus tipo 2	DM2 diagnosticada 2020	2020-11-10	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
5	3	Medicamento	Metformina	850mg cada 12 horas	2020-11-10	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
6	5	Patologia	Asma	Asma moderada persistente	2015-08-05	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
7	5	Medicamento	Salbutamol	Inhalador de rescate	2015-08-05	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
8	8	Patologia	Epilepsia	Desde adolescencia	2008-03-12	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
9	11	Patologia	Dislipidemia	Colesterol elevado	2018-01-20	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
10	13	Cirugia	Apendicectomia	Cirugia laparoscopica	2015-07-10	f	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
11	17	Alergia	Yodo	Reaccion cutanea	2012-09-15	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
12	19	Patologia	Artritis reumatoide	Diagnosticada 2019	2019-04-22	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
13	25	Patologia	Arritmia	FA paroxistica	2020-02-14	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
14	28	Alergia	Latex	Anafilaxia leve	2015-12-03	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
15	31	Patologia	EPOC	Enfermedad pulmonar cronica	2017-11-18	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
16	35	Patologia	Bronquitis cronica	Fumador ex 20 paquetes-aÃ±o	2016-09-25	t	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
17	38	Cirugia	Colecistectomia	Por colelitiasis	2010-05-15	f	2026-05-03 00:02:55.42529	2026-05-03 00:02:55.42529	1
\.


--
-- Data for Name: hce_consulta_previa; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.hce_consulta_previa (id, paciente_id, fecha_consulta, motivo, diagnostico_medico, tratamiento, created_at, updated_at, version, activo) FROM stdin;
1	1	2023-08-15 09:00:00	Control de hipertension	HTA compensada	Continuar Losartan 50mg	2026-05-03 00:02:55.430769	2026-05-03 00:02:55.430769	1	t
2	3	2023-06-20 14:00:00	Control DM2	DM2 compensada HbA1c 7.2%	Continuar Metformina	2026-05-03 00:02:55.430769	2026-05-03 00:02:55.430769	1	t
3	5	2023-09-12 11:00:00	Exacerbacion asmatica	Asma moderada	Prednisona 5 dias	2026-05-03 00:02:55.430769	2026-05-03 00:02:55.430769	1	t
4	8	2023-07-25 16:00:00	Control epilepsia	Epilepsia estable	Continuar valproato	2026-05-03 00:02:55.430769	2026-05-03 00:02:55.430769	1	t
5	11	2023-10-08 10:00:00	Control dislipidemia	Dislipidemia mejorada	Continuar estatina	2026-05-03 00:02:55.430769	2026-05-03 00:02:55.430769	1	t
6	19	2023-05-18 09:15:00	Control artritis	AR actividad moderada	Ajustar MTX	2026-05-03 00:02:55.430769	2026-05-03 00:02:55.430769	1	t
7	25	2023-08-22 14:30:00	Palpitaciones	FA paroxistica	Anticoagulante iniciado	2026-05-03 00:02:55.430769	2026-05-03 00:02:55.430769	1	t
8	31	2023-09-30 11:45:00	Exacerbacion EPOC	EPOC exacerbada	Corticoides + antibiotico	2026-05-03 00:02:55.430769	2026-05-03 00:02:55.430769	1	t
9	38	2023-04-12 10:30:00	Colico nefritico	Calculo renal	Analgesicos + hidratacion	2026-05-03 00:02:55.430769	2026-05-03 00:02:55.430769	1	t
10	40	2023-07-08 09:00:00	Control ACV	Secuelas leves	Rehabilitacion	2026-05-03 00:02:55.430769	2026-05-03 00:02:55.430769	1	t
\.


--
-- Data for Name: logs_auditoria; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.logs_auditoria (id, usuario_id, accion, modulo, registro_id, datos_anteriores, datos_nuevos, ip_address, user_agent, "timestamp") FROM stdin;
1	2	INSERT	triajes	1	\N	{"nivel": "RED", "paciente_id": 1}	192.168.1.10	Mozilla/5.0	2026-05-02 22:02:55.436464
2	2	UPDATE	triajes	1	{"estado": "En Espera"}	{"estado": "En Atencion"}	192.168.1.10	Mozilla/5.0	2026-05-02 22:32:55.436464
3	2	UPDATE	triajes	1	{"estado": "En Atencion"}	{"estado": "Atendido"}	192.168.1.10	Mozilla/5.0	2026-05-02 23:32:55.436464
4	3	INSERT	triajes	2	\N	{"nivel": "YELLOW", "paciente_id": 2}	192.168.1.11	Mozilla/5.0	2026-05-02 21:02:55.436464
5	3	UPDATE	triajes	2	{"nivel_ia": "RED", "nivel_final": null}	{"nivel_ia": "RED", "nivel_final": "YELLOW"}	192.168.1.11	Mozilla/5.0	2026-05-02 21:32:55.436464
6	4	INSERT	triajes	4	\N	{"nivel": "GREEN", "paciente_id": 4}	192.168.1.12	Mozilla/5.0	2026-05-02 19:02:55.436464
7	4	INSERT	signos_vitales	4	\N	{"fc": 75, "triaje_id": 4}	192.168.1.12	Mozilla/5.0	2026-05-02 19:17:55.436464
8	2	STATUS_CHANGE	triajes	8	{"estado": "En Espera"}	{"estado": "Llamado"}	192.168.1.10	Mozilla/5.0	2026-05-02 23:42:55.436464
9	3	STATUS_CHANGE	triajes	8	{"estado": "Llamado"}	{"estado": "En Atencion"}	192.168.1.11	Mozilla/5.0	2026-05-02 23:57:55.436464
10	3	INSERT	triajes	8	\N	{"nivel": "RED", "paciente_id": 8}	192.168.1.20	Mozilla/5.0	2026-05-02 23:17:55.436464
11	2	INSERT	triajes	9	\N	{"nivel": "GREEN", "paciente_id": 9}	192.168.1.21	Mozilla/5.0	2026-05-02 23:52:55.436464
12	1	INSERT	triajes	40	\N	{"nivel": "RED", "paciente_id": 40}	192.168.1.50	PostmanRuntime/7.36.0	2023-12-19 16:00:00
13	7	INSERT	triajes	11	\N	{"nivel": "RED", "paciente_id": 11}	192.168.1.17	Mozilla/5.0	2024-02-15 14:30:00
14	7	UPDATE	triajes	11	{"estado": "En Espera"}	{"estado": "Atendido"}	192.168.1.17	Mozilla/5.0	2024-02-15 15:30:00
15	2	INSERT	triaje	41	null	{"motivo": "Dolor Torácico", "paciente_id": 1}	\N	\N	2026-05-03 02:21:16.944768
16	2	UPDATE	triaje	41	{"estado_logistico": "En Espera", "nivel_urgencia_final": "YELLOW"}	{"estado_logistico": "En Espera", "nivel_urgencia_final": "YELLOW"}	\N	\N	2026-05-03 02:21:31.004026
17	2	INSERT	paciente	51	null	"{\\"dni\\":\\"75645353\\",\\"nombres\\":\\"FAVIAN\\",\\"apellidos\\":\\"VALDIVIEZO\\",\\"fecha_nacimiento\\":\\"2016-05-10\\",\\"genero\\":\\"M\\",\\"telefono\\":\\"90173663\\",\\"email\\":\\"RealGoat@unitru.edu.pe\\",\\"direccion\\":\\"Prol. Sinchi Roca, La Libertad\\\\n\\",\\"contactos_emergencia\\":[]}"	\N	\N	2026-05-03 02:24:28.559015
18	2	INSERT	triaje	42	null	{"motivo": "Sangre incontrolable por la nariz", "paciente_id": 51}	\N	\N	2026-05-03 02:25:32.193686
19	2	UPDATE	triaje	42	{"estado_logistico": "En Espera", "nivel_urgencia_final": "YELLOW"}	{"estado_logistico": "En Espera", "nivel_urgencia_final": "YELLOW"}	\N	\N	2026-05-03 02:25:50.841265
20	2	INSERT	triaje	43	null	{"motivo": "Dolor torácico", "paciente_id": 1}	\N	\N	2026-05-03 02:35:26.183555
21	2	UPDATE	triaje	43	{"estado_logistico": "En Espera", "nivel_urgencia_final": "ORANGE"}	{"estado_logistico": "En Espera", "nivel_urgencia_final": "YELLOW"}	\N	\N	2026-05-03 02:35:36.262718
22	4	STATUS_CHANGE	estado_logistico	8	{"estado_anterior": "Llamado"}	{"estado_nuevo": "En Atencion"}	\N	\N	2026-05-03 03:18:10.374449
23	2	INSERT	triaje	44	null	{"motivo": "Dolor torácico", "paciente_id": 1}	\N	\N	2026-05-04 12:14:33.276604
24	2	UPDATE	triaje	44	{"estado_logistico": "En Espera", "nivel_urgencia_final": "ORANGE"}	{"estado_logistico": "En Espera", "nivel_urgencia_final": "RED"}	\N	\N	2026-05-04 12:14:51.402193
25	4	STATUS_CHANGE	estado_logistico	44	{"estado_anterior": "En Espera"}	{"estado_nuevo": "Llamado"}	\N	\N	2026-05-04 12:30:41.680732
26	4	UPDATE	notas_medicas	8	null	{"notas": "Posible asma severo. Oxigenoterapia iniciada.", "diagnostico": "Gostrointeritis"}	\N	\N	2026-05-04 12:31:19.322377
27	4	STATUS_CHANGE	estado_logistico	8	{"estado_anterior": "En Atencion"}	{"estado_nuevo": "Atendido"}	\N	\N	2026-05-04 12:31:23.539232
28	2	INSERT	paciente	52	null	"{\\"dni\\":\\"76534332\\",\\"nombres\\":\\"FAVIAN\\",\\"apellidos\\":\\"VALDIVIEZO\\",\\"fecha_nacimiento\\":\\"2011-05-17\\",\\"genero\\":\\"M\\",\\"telefono\\":\\"9876543437\\",\\"email\\":\\"fevillava@unitru.edu.pe\\",\\"direccion\\":\\"Prol. Sinchi Roca, La Libertad\\\\n\\",\\"contactos_emergencia\\":[]}"	\N	\N	2026-05-04 12:46:27.250804
29	2	INSERT	paciente	53	null	"{\\"dni\\":\\"76543324\\",\\"nombres\\":\\"FAVIAN\\",\\"apellidos\\":\\"VALDIVIEZO\\",\\"fecha_nacimiento\\":\\"2011-05-17\\",\\"genero\\":\\"M\\",\\"telefono\\":\\"9876543437\\",\\"email\\":\\"fevillava@unitru.edu.pe\\",\\"direccion\\":\\"Prol. Sinchi Roca, La Libertad\\\\n\\",\\"contactos_emergencia\\":[]}"	\N	\N	2026-05-04 12:46:45.506869
30	2	INSERT	triaje	45	null	{"motivo": "Dolor torácico", "paciente_id": 53}	\N	\N	2026-05-04 12:58:12.869765
31	2	INSERT	paciente	54	null	"{\\"dni\\":\\"75675435\\",\\"nombres\\":\\"Villa\\",\\"apellidos\\":\\"Favian\\",\\"fecha_nacimiento\\":\\"2002-01-10\\",\\"genero\\":\\"M\\",\\"telefono\\":\\"904354554\\",\\"email\\":\\"villafavian87@gmail.com\\",\\"direccion\\":\\"Shinchi Roca\\",\\"contactos_emergencia\\":[]}"	\N	\N	2026-05-08 02:12:50.818106
32	2	INSERT	triaje	46	null	{"motivo": "Dolor torácico", "paciente_id": 54}	\N	\N	2026-05-08 02:13:34.311831
33	2	UPDATE	triaje	46	{"estado_logistico": "En Espera", "nivel_urgencia_final": "RED"}	{"estado_logistico": "En Espera", "nivel_urgencia_final": "RED"}	\N	\N	2026-05-08 02:13:50.023434
34	4	UPDATE	notas_medicas	6	null	{"notas": "Dolor craneal intenso. Analgesico administrado.", "diagnostico": "Dolor de Cabeza"}	\N	\N	2026-05-08 02:18:03.837886
35	4	UPDATE	notas_medicas	6	null	{"notas": "Dolor craneal intenso. Analgesico administrado.", "diagnostico": "Dolor de Cabeza"}	\N	\N	2026-05-08 02:18:11.35845
36	4	UPDATE	notas_medicas	6	null	{"notas": "Dolor craneal intenso. Analgesico administrado.", "diagnostico": "Dolor de Cabeza"}	\N	\N	2026-05-08 02:18:18.135117
37	4	STATUS_CHANGE	estado_logistico	6	{"estado_anterior": "En Atencion"}	{"estado_nuevo": "Atendido"}	\N	\N	2026-05-08 02:18:22.30296
\.


--
-- Data for Name: pacientes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.pacientes (id, dni, nombres, apellidos, fecha_nacimiento, genero, telefono, email, direccion, activo, created_at, updated_at, version) FROM stdin;
1	12345678	Juan	Martinez	1985-03-15	M	555-0101	juan.martinez@email.com	Av. Principal 123, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
2	23456789	Maria	Lopez	1990-07-22	F	555-0102	maria.lopez@email.com	Jr. Comercio 456, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
3	34567890	Carlos	Garcia	1978-11-05	M	555-0103	carlos.garcia@email.com	Calle Real 789, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
4	45678901	Ana	Rodriguez	1995-01-30	F	555-0104	ana.rodriguez@email.com	Av. Las Flores 321, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
5	56789012	Luis	Sanchez	1982-09-12	M	555-0105	luis.sanchez@email.com	Jr. Paris 654, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
6	67890123	Carmen	Perez	1988-04-18	F	555-0106	carmen.perez@email.com	Calle Lima 987, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
7	78901234	Pedro	Fernandez	1975-12-25	M	555-0107	pedro.fernandez@email.com	Av. Arequipa 147, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
8	89012345	Sofia	Gonzalez	1992-06-08	F	555-0108	sofia.gonzalez@email.com	Jr. Washington 258, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
9	90123456	Miguel	Ramirez	1980-02-14	M	555-0109	miguel.ramirez@email.com	Calle Junin 369, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
10	01234567	Laura	Torres	1993-10-20	F	555-0110	laura.torres@email.com	Av. Tacna 741, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
11	11223344	Roberto	Vargas	1968-08-03	M	555-0111	roberto.vargas@email.com	Jr. Ica 852, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
12	22334455	Diana	Castro	1986-11-27	F	555-0112	diana.castro@email.com	Calle Piura 963, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
13	33445566	Jorge	Morales	1979-05-16	M	555-0113	jorge.morales@email.com	Av. Cusco 159, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
14	44556677	Gabriela	Ortega	1991-03-09	F	555-0114	gabriela.ortega@email.com	Jr. Tumbes 357, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
15	55667788	Fernando	Herrera	1984-07-31	M	555-0115	fernando.herrera@email.com	Calle Trujillo 486, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
16	66778899	Patricia	Silva	1977-01-23	F	555-0116	patricia.silva@email.com	Av. Chiclayo 753, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
17	77889900	Ricardo	Mendoza	1994-09-05	M	555-0117	ricardo.mendoza@email.com	Jr. Puno 951, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
18	88990011	Isabel	Rojas	1983-12-11	F	555-0118	isabel.rojas@email.com	Calle Cajamarca 357, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
19	99001122	Hugo	Guerrero	1976-04-29	M	555-0119	hugo.guerrero@email.com	Av. Loreto 159, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
20	00112233	Monica	Cruz	1989-08-17	F	555-0120	monica.cruz@email.com	Jr. Ucayali 753, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
21	12345001	Alejandro	Reyes	1972-02-08	M	555-0121	alejandro.reyes@email.com	Calle Amazonas 456, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
22	23456002	Valentina	Navarro	1996-06-25	F	555-0122	valentina.navarro@email.com	Av. Madre de Dios 789, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
23	34567003	Santiago	Aguirre	1981-10-13	M	555-0123	santiago.aguirre@email.com	Jr. San Martin 321, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
24	45678004	Camila	Delgado	1987-03-04	F	555-0124	camila.delgado@email.com	Calle Huanuco 654, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
25	56789005	Martin	Paredes	1974-07-19	M	555-0125	martin.paredes@email.com	Av. Pasco 987, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
26	67890006	Luciana	Vega	1990-11-22	F	555-0126	luciana.vega@email.com	Jr. Huancavelica 147, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
27	78901007	Emiliano	Flores	1986-01-14	M	555-0127	emiliano.flores@email.com	Calle Ayacucho 258, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
28	89012008	Mariana	Espinoza	1993-05-28	F	555-0128	mariana.espinoza@email.com	Av. Apurimac 369, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
29	90123009	Leonardo	Soto	1978-09-10	M	555-0129	leonardo.soto@email.com	Jr. Huancayo 741, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
30	01234010	Victoria	Caceres	1985-12-02	F	555-0130	victoria.caceres@email.com	Calle Huacho 852, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
31	13579001	Andres	Valenzuela	1970-04-16	M	555-0131	andres.valenzuela@email.com	Av. Chimbote 159, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
32	24680002	Daniela	Bravo	1997-08-24	F	555-0132	daniela.bravo@email.com	Jr. Nazca 357, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
33	35790003	Felipe	Araya	1982-12-07	M	555-0133	felipe.araya@email.com	Calle Iquitos 486, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
34	46801004	Antonella	Pena	1988-03-21	F	555-0134	antonella.pena@email.com	Av. Pucallpa 753, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
35	57912005	Maximiliano	Carrasco	1975-06-14	M	555-0135	maximiliano.carrasco@email.com	Jr. Tarapoto 951, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
36	68023006	Julieta	Sandoval	1992-10-09	F	555-0136	julieta.sandoval@email.com	Calle Moyobamba 357, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
37	79134007	Agustin	Tapia	1980-02-27	M	555-0137	agustin.tapia@email.com	Av. Yurimaguas 159, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
38	80245008	Martina	Zuniga	1994-07-03	F	555-0138	martina.zuniga@email.com	Jr. Jaen 753, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
39	91356009	Benjamin	Contreras	1973-11-18	M	555-0139	benjamin.contreras@email.com	Calle Bagua 951, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
40	02467010	Emilia	Figueroa	1987-01-06	F	555-0140	emilia.figueroa@email.com	Av. Bagua Grande 357, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
41	13578111	Damian	Sepulveda	1998-05-11	M	555-0141	damian.sepulveda@email.com	Jr. Chachapoyas 159, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
42	24689222	Renata	Cardenas	1971-09-29	F	555-0142	renata.cardenas@email.com	Calle Moyobamba 753, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
43	35790333	Thiago	Salazar	1984-02-02	M	555-0143	thiago.salazar@email.com	Av. Rioja 951, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
44	46801444	Olivia	Maldonado	1995-06-17	F	555-0144	olivia.maldonado@email.com	Jr. Lambayeque 357, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
45	57912555	Benicio	Escobar	1977-10-05	M	555-0145	benicio.escobar@email.com	Calle Ferrenafe 159, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
46	68023666	Alma	Palacios	1991-12-23	F	555-0146	alma.palacios@email.com	Jr. Chicama 753, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
47	79134777	Bautista	Guzman	1969-08-12	M	555-0147	bautista.guzman@email.com	Av. Viru 951, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
48	80245888	Celeste	Escudero	1983-04-01	F	555-0148	celeste.escudero@email.com	Calle Guadalupe 357, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
49	91356999	Ciro	Miranda	1999-12-19	M	555-0149	ciro.miranda@email.com	Jr. Chepen 159, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
50	02467100	Emma	Peralta	1987-05-20	F	555-0150	emma.peralta@email.com	Calle Chota 753, Lima	t	2026-05-03 00:02:55.291783	2026-05-03 00:02:55.291783	1
51	75645353	FAVIAN	VALDIVIEZO	2016-05-10	M	90173663	RealGoat@unitru.edu.pe	Prol. Sinchi Roca, La Libertad\n	t	2026-05-03 02:24:28.525648	2026-05-03 02:24:28.525648	1
52	76534332	FAVIAN	VALDIVIEZO	2011-05-17	M	9876543437	fevillava@unitru.edu.pe	Prol. Sinchi Roca, La Libertad\n	t	2026-05-04 12:46:27.158638	2026-05-04 12:46:27.158638	1
53	76543324	FAVIAN	VALDIVIEZO	2011-05-17	M	9876543437	fevillava@unitru.edu.pe	Prol. Sinchi Roca, La Libertad\n	t	2026-05-04 12:46:45.495075	2026-05-04 12:46:45.495075	1
54	75675435	Villa	Favian	2002-01-10	M	904354554	villafavian87@gmail.com	Shinchi Roca	t	2026-05-08 02:12:50.741669	2026-05-08 02:12:50.741669	1
\.


--
-- Data for Name: resultados_ia; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.resultados_ia (id, triaje_id, prompt_enviado, respuesta_raw_llm, diagnosticos_json, recomendaciones_json, modelo_utilizado, latencia_segundos, created_at, updated_at, activo, version) FROM stdin;
1	1	Prompt: Paciente masculino 38 aÃ±os...	RESPONSE: Nivel RED	[{"diagnostico": "Sindrome coronario agudo", "probabilidad": 0.85}]	[{"accion": "ECG 12 derivaciones", "prioridad": "inmediata"}]	gpt-4	2.50	2026-05-03 00:02:55.420285	2026-05-03 00:02:55.420285	t	1
2	3	Prompt: Paciente masculino 45 aÃ±os...	RESPONSE: Nivel RED	[{"diagnostico": "Apendicitis aguda", "probabilidad": 0.80}]	[{"accion": "Cirugia de emergencia", "prioridad": "urgente"}]	gpt-4	2.20	2026-05-03 00:02:55.420285	2026-05-03 00:02:55.420285	t	1
3	11	Prompt: Paciente masculino 55 aÃ±os...	RESPONSE: Nivel RED	[{"diagnostico": "IAM", "probabilidad": 0.90}]	[{"accion": "Trombolisis", "prioridad": "inmediata"}]	gpt-4	2.10	2026-05-03 00:02:55.420285	2026-05-03 00:02:55.420285	t	1
4	13	Prompt: Paciente masculino 45 aÃ±os...	RESPONSE: Nivel RED	[{"diagnostico": "TCE severo", "probabilidad": 0.88}]	[{"accion": "TAC craneo", "prioridad": "inmediata"}]	gpt-4	2.80	2026-05-03 00:02:55.420285	2026-05-03 00:02:55.420285	t	1
5	18	Prompt: Paciente masculino 44 aÃ±os...	RESPONSE: Nivel RED	[{"diagnostico": "Crisis epileptica", "probabilidad": 0.92}]	[{"accion": "Diazepam 10mg IV", "prioridad": "inmediata"}]	gpt-4	1.90	2026-05-03 00:02:55.420285	2026-05-03 00:02:55.420285	t	1
6	22	Prompt: Paciente masculino 46 aÃ±os...	RESPONSE: Nivel RED	[{"diagnostico": "Trauma penetrante", "probabilidad": 0.95}]	[{"accion": "Laparotomia", "prioridad": "inmediata"}]	gpt-4	2.30	2026-05-03 00:02:55.420285	2026-05-03 00:02:55.420285	t	1
7	28	Prompt: Paciente femenina 31 aÃ±os...	RESPONSE: Nivel RED	[{"diagnostico": "HSA", "probabilidad": 0.87}]	[{"accion": "TAC urgente", "prioridad": "inmediata"}]	gpt-4	2.00	2026-05-03 00:02:55.420285	2026-05-03 00:02:55.420285	t	1
8	40	Prompt: Paciente femenina 37 aÃ±os...	RESPONSE: Nivel RED	[{"diagnostico": "ACV isquemico", "probabilidad": 0.91}]	[{"accion": "Trombolisis IV", "prioridad": "inmediata"}]	gpt-4	2.40	2026-05-03 00:02:55.420285	2026-05-03 00:02:55.420285	t	1
9	41		{"nivel_urgencia":"YELLOW","diagnosticos":["Síndrome doloroso torácico"],"recomendaciones":"Evaluar causa del dolor torácico, considerar electrocardiograma y marcadores cardiacos","signos_alarma":["dolor torácico persistente","disnea"],"requiere_aislamiento":false}	{"diagnosticos": ["Síndrome doloroso torácico"]}	{"recomendaciones": "Evaluar causa del dolor torácico, considerar electrocardiograma y marcadores cardiacos"}	llama-3.3-70b-versatile	1.02	2026-05-03 02:21:15.749778	2026-05-03 02:21:15.749778	t	1
10	42		{"nivel_urgencia":"YELLOW","diagnosticos":["Epistaxis"],"recomendaciones":"Evaluar causa de sangrado nasal, considerar tamponamiento nasal o cauterización si necesario","signos_alarma":["Hemorragia masiva","Dificultad respiratoria"],"requiere_aislamiento":false}	{"diagnosticos": ["Epistaxis"]}	{"recomendaciones": "Evaluar causa de sangrado nasal, considerar tamponamiento nasal o cauterización si necesario"}	llama-3.3-70b-versatile	0.70	2026-05-03 02:25:31.438699	2026-05-03 02:25:31.438699	t	1
11	43		{"nivel_urgencia":"ORANGE","diagnosticos":["Síndrome doloroso torácico"],"recomendaciones":"Evaluar causa del dolor torácico, considerar prueba de esfuerzo o ecocardiograma","signos_alarma":["dolor torácico","mareos"],"requiere_aislamiento":false}	{"diagnosticos": ["Síndrome doloroso torácico"]}	{"recomendaciones": "Evaluar causa del dolor torácico, considerar prueba de esfuerzo o ecocardiograma"}	llama-3.3-70b-versatile	0.63	2026-05-03 02:35:25.505507	2026-05-03 02:35:25.505507	t	1
12	44		{"nivel_urgencia":"ORANGE","diagnosticos":["Síndrome doloroso torácico"],"recomendaciones":"Evaluar causa del dolor torácico, considerar posibilidad de enfermedad cardíaca o pulmonar","signos_alarma":["dolor torácico","nauseas","cefalea"],"requiere_aislamiento":false}	{"diagnosticos": ["Síndrome doloroso torácico"]}	{"recomendaciones": "Evaluar causa del dolor torácico, considerar posibilidad de enfermedad cardíaca o pulmonar"}	llama-3.3-70b-versatile	2.50	2026-05-04 12:14:27.582216	2026-05-04 12:14:27.582216	t	1
13	45		{"nivel_urgencia":"RED","diagnosticos":["Síndrome doloroso torácico","Síndrome febril agudo"],"recomendaciones":"Evaluar inmediatamente por posible infección o infarto, realizar ECG y tomar muestra para hemocultivo","signos_alarma":["dolor torácico","fiebre alta","taquicardia"],"requiere_aislamiento":true}	{"diagnosticos": ["Síndrome doloroso torácico", "Síndrome febril agudo"]}	{"recomendaciones": "Evaluar inmediatamente por posible infección o infarto, realizar ECG y tomar muestra para hemocultivo"}	llama-3.3-70b-versatile	1.13	2026-05-04 12:58:09.088439	2026-05-04 12:58:09.088439	t	1
14	46		{"nivel_urgencia":"RED","diagnosticos":["Síndrome doloroso torácico agudo"],"recomendaciones":"Evaluar inmediatamente por posible infarto de miocardio o otra causa grave","signos_alarma":["dolor torácico","taquicardia"],"requiere_aislamiento":false}	{"diagnosticos": ["Síndrome doloroso torácico agudo"]}	{"recomendaciones": "Evaluar inmediatamente por posible infarto de miocardio o otra causa grave"}	llama-3.3-70b-versatile	1.32	2026-05-08 02:13:30.374175	2026-05-08 02:13:30.374175	t	1
\.


--
-- Data for Name: signos_vitales; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.signos_vitales (id, triaje_id, presion_sistolica, presion_diastolica, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, saturacion_o2, nota_suplementaria, created_at, updated_at, activo, version) FROM stdin;
1	1	180	110	110	24	37.2	95	Hipertension severa	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
2	2	130	85	95	20	39.1	98	Fiebre alta	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
3	3	140	90	105	22	38.0	97	Dolor abdominal	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
4	4	120	80	75	18	37.0	99	Estable	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
5	5	125	82	88	19	36.8	100	Dolor moderado	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
6	6	118	78	72	16	36.5	99	Dolor craneal	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
7	7	128	84	92	20	37.1	98	Quemadura	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
8	8	110	75	115	28	37.0	88	Dificultad respiratoria	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
9	9	122	80	70	18	36.7	100	Lesion leve	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
10	10	124	82	78	19	37.2	99	Deshidratacion leve	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
11	11	160	100	105	22	37.0	94	Infarto	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
12	12	118	76	82	18	37.5	99	Faringitis	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
13	13	90	60	120	25	36.0	92	Trauma craneal	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
14	14	128	82	78	18	36.8	98	Dolor lumbar	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
15	15	135	88	95	20	37.0	97	Epistaxis	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
16	16	85	55	115	24	36.5	93	Anafilaxia	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
17	17	120	78	72	18	37.2	99	Otitis	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
18	18	140	90	125	22	38.5	96	Convulsiones	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
19	19	132	86	80	19	36.9	98	Artritis	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
20	20	145	92	100	24	37.8	95	Hemoptisis	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
21	21	110	70	95	20	36.5	97	Sincope	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
22	22	80	50	130	30	35.0	85	Shock hemorragico	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
23	23	125	80	88	19	37.6	99	Infeccion urinaria	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
24	24	120	78	76	18	36.8	100	Dolor ocular	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
25	25	138	88	110	22	37.1	97	Arritmia	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
26	26	122	80	70	18	36.5	100	Trauma leve	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
27	27	118	76	85	20	37.4	98	Gastroenteritis	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
28	28	175	105	115	24	37.0	94	Hemorragia cerebral	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
29	29	120	78	74	18	37.0	99	Alergia	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
30	30	140	90	105	26	37.2	91	Neumotorax	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
31	31	110	72	88	20	37.8	98	Intoxicacion	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
32	32	115	75	70	16	36.5	99	Contractura	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
33	33	125	82	78	18	37.0	100	Trauma ocular	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
34	34	135	88	125	28	36.0	90	Electrocucion	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
35	35	118	78	95	24	37.5	96	Bronquitis	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
36	36	120	80	72	18	37.0	99	Dolor dental	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
37	37	95	60	55	12	33.0	92	Hipotermia	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
38	38	128	85	100	22	38.0	97	Calculo renal	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
39	39	122	78	68	16	36.5	99	Insomnio	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
40	40	70	45	140	32	35.5	88	Shock traumatico	2026-05-03 00:02:55.406982	2026-05-03 00:02:55.406982	t	1
41	41	120	80	80	16	36.5	97	\N	2026-05-03 02:21:15.749778	2026-05-03 02:21:15.749778	t	1
42	42	120	80	80	16	36.5	97	\N	2026-05-03 02:25:31.438699	2026-05-03 02:25:31.438699	t	1
43	43	120	80	80	16	36.5	97	\N	2026-05-03 02:35:25.505507	2026-05-03 02:35:25.505507	t	1
44	44	120	80	80	16	36.5	97	\N	2026-05-04 12:14:27.582216	2026-05-04 12:14:27.582216	t	1
45	45	120	80	120	16	40.0	97	\N	2026-05-04 12:58:09.088439	2026-05-04 12:58:09.088439	t	1
46	46	120	80	120	16	36.5	97	\N	2026-05-08 02:13:30.374175	2026-05-08 02:13:30.374175	t	1
\.


--
-- Data for Name: sintomas_triaje; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.sintomas_triaje (id, triaje_id, sintoma, intensidad, descripcion_libre, created_at, updated_at, activo, version) FROM stdin;
1	1	Dolor toracico	Grave	Oprimido, irradia a brazo izquierdo	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
2	1	Sudoracion	Moderado	Sudoracion profusa	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
3	1	Nauseas	Leve	\N	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
4	2	Fiebre	Moderado	39C desde hace 2 dias	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
5	2	Dolor de cabeza	Moderado	Frontal y constante	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
6	2	Malestar general	Moderado	\N	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
7	3	Dolor abdominal	Grave	Fosa iliaca derecha	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
8	3	Vomitos	Moderado	Alimentarios	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
9	3	Fiebre	Leve	37.8C	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
10	4	Tos	Leve	Productiva	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
11	4	Congestion nasal	Leve	\N	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
12	5	Dolor	Grave	Intenso en antebrazo	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
13	5	Deformidad	Moderado	Angulacion visible	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
14	6	Dolor de cabeza	Grave	Pulsatil unilateral	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
15	6	Fotofobia	Moderado	Intolerancia a la luz	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
16	8	Disnea	Grave	Dificultad para respirar	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
17	8	Sibilancias	Moderado	Al espirar	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
18	11	Dolor toracico	Grave	Tipo opresivo	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
19	13	Alteracion conciencia	Grave	Glasgow 12	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
20	13	Dolor de cabeza	Grave	Intenso	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
21	14	Dolor lumbar	Moderado	Irradia a gluteo	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
22	18	Convulsiones	Grave	Tonico-clonicas generalizadas	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
23	22	Dolor	Grave	Herida de bala en abdomen	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
24	22	Hemorragia	Grave	Activa	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
25	28	Cefalea explosiva	Grave	Peor dolor de su vida	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
26	28	Rigidez de nuca	Grave	\N	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
27	30	Dolor toracico	Grave	Pleuritico	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
28	30	Disnea	Grave	Repentina	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
29	34	Quemadura	Grave	Entrada y salida	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
30	40	Amputacion	Grave	Dedos de mano derecha	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
31	28	Deficit motor	Moderado	Debilidad en brazo izquierdo	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
32	30	Afasia	Leve	Dificultad para hablar	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
33	38	Vomito	Moderado	Nauseas persistentes	2026-05-03 00:02:55.412975	2026-05-03 00:02:55.412975	t	1
34	41	Fiebre	Leve	\N	2026-05-03 02:21:15.749778	2026-05-03 02:21:15.749778	t	1
35	41	Nauseas	Leve	\N	2026-05-03 02:21:15.749778	2026-05-03 02:21:15.749778	t	1
36	41	Mareos	Leve	\N	2026-05-03 02:21:15.749778	2026-05-03 02:21:15.749778	t	1
37	42	Fiebre	Leve	\N	2026-05-03 02:25:31.438699	2026-05-03 02:25:31.438699	t	1
38	42	Nauseas	Leve	\N	2026-05-03 02:25:31.438699	2026-05-03 02:25:31.438699	t	1
39	42	Mareos	Leve	\N	2026-05-03 02:25:31.438699	2026-05-03 02:25:31.438699	t	1
40	43	Nauseas	Moderado	\N	2026-05-03 02:35:25.505507	2026-05-03 02:35:25.505507	t	1
41	43	Mareos	Grave	\N	2026-05-03 02:35:25.505507	2026-05-03 02:35:25.505507	t	1
42	43	Fiebre	Grave	\N	2026-05-03 02:35:25.505507	2026-05-03 02:35:25.505507	t	1
43	44	Nauseas	Grave	\N	2026-05-04 12:14:27.582216	2026-05-04 12:14:27.582216	t	1
44	44	Cefalea	Grave	\N	2026-05-04 12:14:27.582216	2026-05-04 12:14:27.582216	t	1
45	44	Fiebre	Grave	\N	2026-05-04 12:14:27.582216	2026-05-04 12:14:27.582216	t	1
46	45	Nauseas	Grave	\N	2026-05-04 12:58:09.088439	2026-05-04 12:58:09.088439	t	1
47	45	Mareos	Grave	\N	2026-05-04 12:58:09.088439	2026-05-04 12:58:09.088439	t	1
48	45	Fiebre	Grave	\N	2026-05-04 12:58:09.088439	2026-05-04 12:58:09.088439	t	1
49	46	Dolor_abdominal	Moderado	\N	2026-05-08 02:13:30.374175	2026-05-08 02:13:30.374175	t	1
\.


--
-- Data for Name: triajes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.triajes (id, paciente_id, usuario_id, fecha_hora, motivo_consulta, nivel_urgencia_asignado_ia, nivel_urgencia_final, estado_logistico, notas_medicas, diagnostico_final_medico, tiempo_atencion_segundos, activo, created_at, updated_at, version, sincronizado_hce, fecha_sincronizacion_hce, hce_sync, hce_sync_at) FROM stdin;
4	4	4	2026-05-02 19:02:55.360225	Tos y congestion nasal	GREEN	GREEN	Atendido	Resfriado comun. Reposo indicado.	\N	600	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
5	5	3	2026-05-02 18:02:55.360225	Fractura de brazo	YELLOW	YELLOW	Atendido	Fractura de cubito. Yesado aplicado.	\N	1800	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
7	7	4	2026-05-02 23:32:55.360225	Quemadura de segundo grado	YELLOW	YELLOW	En Atencion	Quemadura en antebrazo. Curacion en proceso.	\N	900	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
10	10	4	2026-05-02 23:47:55.360225	Nauseas y vomitos	GREEN	GREEN	En Espera	Gastroenteritis probable. Hidratacion oral.	\N	\N	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
12	12	3	2024-02-14 09:15:00	Dolor de garganta	GREEN	GREEN	Atendido	Faringitis estreptococica. Antibiotico prescrito.	\N	540	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
16	16	4	2024-02-10 19:30:00	Alergia alimentaria	YELLOW	YELLOW	Atendido	Shock anafilactico. Adrenalina administrada.	\N	480	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
19	19	4	2024-02-07 15:20:00	Dolor articular	GREEN	GREEN	Atendido	Artritis reumatoide. AINEs indicados.	\N	720	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
20	20	2	2024-02-06 07:45:00	Hemoptisis	ORANGE	ORANGE	Atendido	Tuberculosis sospechada. Aislamiento indicado.	\N	1200	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
21	21	3	2024-01-25 12:00:00	Sincope	ORANGE	ORANGE	Atendido	Perdida de conciencia breve. Estudio cardiologico.	\N	840	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
23	23	4	2024-01-23 09:00:00	Infeccion urinaria	YELLOW	YELLOW	Atendido	Cistitis. Antibiotico oral prescrito.	\N	540	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
24	24	3	2024-01-22 14:15:00	Dolor ocular	YELLOW	YELLOW	Atendido	Uveitis. Derivar a oftalmologia.	\N	660	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
26	26	4	2024-01-20 16:45:00	Esguince de tobillo	GREEN	GREEN	Atendido	Trauma leve. Vendaje compresivo.	\N	600	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
27	27	3	2024-01-19 08:30:00	Dolor abdominal difuso	YELLOW	YELLOW	Atendido	Gastroenteritis. Hidratacion IV.	\N	900	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
29	29	4	2024-01-17 10:30:00	Erupcion cutanea	GREEN	GREEN	Atendido	Dermatitis alergica. Antihistaminico.	\N	480	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
30	30	3	2024-01-16 13:00:00	Dolor toracico pleuritico	ORANGE	ORANGE	Atendido	Neumotorax. Drenaje toracico.	\N	2100	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
31	31	2	2023-12-28 15:30:00	Intoxicacion alimentaria	GREEN	GREEN	Atendido	Vomitos y diarrea. Hidratacion.	\N	720	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
33	33	4	2023-12-26 11:20:00	Cuerpo extrano en ojo	YELLOW	YELLOW	Atendido	Extraccion de cuerpo extrano. Antibiotico.	\N	480	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
35	35	3	2023-12-24 14:00:00	Bronquitis aguda	YELLOW	YELLOW	Atendido	Broncoespasmo. Broncodilatadores.	\N	840	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
37	37	2	2023-12-22 17:30:00	Hipotermia	ORANGE	ORANGE	Atendido	Exposicion al frio. Reanimacion.	\N	1200	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
38	38	3	2023-12-21 08:00:00	Calculo renal	YELLOW	YELLOW	Atendido	Colico nefritico. AINEs + espasmoliticos.	\N	1800	t	2026-05-03 00:02:55.360225	2026-05-03 00:02:55.360225	1	f	\N	f	\N
1	1	2	2026-05-01 10:30:00	Dolor de pecho intenso	RED	RED	Atendido	Paciente con sintomas de infarto. Atencion inmediata.	\N	480	t	2026-05-01 10:30:00	2026-05-03 00:06:12.119532	1	f	\N	f	\N
2	2	3	2026-05-01 10:30:00	Fiebre alta y dolor de cabeza	YELLOW	YELLOW	Atendido	Fiebre 39C. Administrado antipiretico.	\N	900	t	2026-05-01 10:30:00	2026-05-03 00:06:12.119532	1	f	\N	f	\N
11	11	2	2026-05-01 10:30:00	Dolor toracico	RED	RED	Atendido	Infarto agudo al miocardio. Trombolisis aplicada.	\N	420	t	2026-05-01 10:30:00	2026-05-03 00:06:12.119532	1	f	\N	f	\N
13	13	4	2026-05-01 10:30:00	Trauma craneoencefalico	RED	RED	Atendido	Accidente de transito. TAC realizado.	\N	1800	t	2026-05-01 10:30:00	2026-05-03 00:06:12.119532	1	f	\N	f	\N
18	18	3	2026-05-01 10:30:00	Convulsiones	RED	RED	Atendido	Crisis epileptica. Diazepam IV administrado.	\N	900	t	2026-05-01 10:30:00	2026-05-03 00:06:12.119532	1	f	\N	f	\N
22	22	2	2026-05-02 14:15:00	Herida de bala	RED	RED	Atendido	Trauma penetrante. Cirugia de emergencia.	\N	3600	t	2026-05-02 14:15:00	2026-05-03 00:06:12.157224	1	f	\N	f	\N
25	25	2	2026-05-02 14:15:00	Palpitaciones	YELLOW	ORANGE	Atendido	Arritmia supraventricular. ECG anormal.	\N	780	t	2026-05-02 14:15:00	2026-05-03 00:06:12.157224	1	f	\N	f	\N
28	28	2	2026-05-02 14:15:00	Cefalea explosiva	RED	RED	Atendido	Hemorragia subaracnoidea. TAC urgente.	\N	1500	t	2026-05-02 14:15:00	2026-05-03 00:06:12.157224	1	f	\N	f	\N
34	34	2	2026-05-02 14:15:00	Quemadura electrica	RED	RED	Atendido	Electrocucion. Monitorizacion cardiaca.	\N	1800	t	2026-05-02 14:15:00	2026-05-03 00:06:12.157224	1	f	\N	f	\N
40	40	2	2026-05-02 14:15:00	Amputacion parcial	RED	RED	Atendido	Trauma laboral. Reimplante no viable.	\N	2400	t	2026-05-02 14:15:00	2026-05-03 00:06:12.157224	1	f	\N	f	\N
3	3	2	2026-05-01 10:30:00	Dolor abdominal agudo	RED	YELLOW	Atendido	Apendicitis aguda. Derivado a cirugia.	\N	1200	t	2026-05-01 10:30:00	2026-05-03 00:06:12.159148	1	f	\N	f	\N
14	14	2	2024-02-12 11:20:00	Dolor lumbar	YELLOW	RED	Atendido	Lumbalgia aguda. AINEs indicados.	\N	780	t	2026-05-03 00:02:55.360225	2026-05-03 00:06:12.160582	1	f	\N	f	\N
6	6	2	2026-05-02 23:02:55.360225	Migrana severa	GREEN	YELLOW	Atendido	Dolor craneal intenso. Analgesico administrado.	Dolor de Cabeza	443726	t	2026-05-03 00:02:55.360225	2026-05-08 02:18:22.254013	5	f	\N	f	\N
15	15	3	2024-02-11 08:00:00	Hemorragia nasal	ORANGE	YELLOW	Atendido	Epistaxis. Tamponado anterior realizado.	\N	660	t	2026-05-03 00:02:55.360225	2026-05-03 00:06:12.163132	1	f	\N	f	\N
9	9	2	2026-05-02 23:52:55.360225	Corte en mano	BLUE	GREEN	En Espera	Laceracion superficial. Esperando curacion.	\N	\N	t	2026-05-03 00:02:55.360225	2026-05-03 00:06:12.164914	1	f	\N	f	\N
17	17	2	2024-02-09 13:45:00	Dolor de oido	BLUE	GREEN	Atendido	Otitis media. Antibiotico topico indicado.	\N	600	t	2026-05-03 00:02:55.360225	2026-05-03 00:06:12.164914	1	f	\N	f	\N
32	32	3	2023-12-27 09:45:00	Dolor de espalda	BLUE	GREEN	Atendido	Contractura muscular. Fisioterapia indicada.	\N	540	t	2026-05-03 00:02:55.360225	2026-05-03 00:06:12.164914	1	f	\N	f	\N
36	36	4	2023-12-23 10:15:00	Dolor dental	BLUE	GREEN	Atendido	Absceso dental. Antibiotico + analgesico.	\N	360	t	2026-05-03 00:02:55.360225	2026-05-03 00:06:12.164914	1	f	\N	f	\N
39	39	4	2023-12-20 13:45:00	Insomnio cronico	BLUE	GREEN	Atendido	Trastorno del sueno. Derivado a psiquiatria.	\N	420	t	2026-05-03 00:02:55.360225	2026-05-03 00:06:12.164914	1	f	\N	f	\N
41	1	2	2026-05-03 02:21:15.769757	Dolor Torácico	YELLOW	YELLOW	En Espera	\N	\N	\N	t	2026-05-03 02:21:15.749778	2026-05-03 02:21:30.979162	2	f	\N	f	\N
42	51	2	2026-05-03 02:25:31.447347	Sangre incontrolable por la nariz	YELLOW	YELLOW	En Espera	\N	\N	\N	t	2026-05-03 02:25:31.438699	2026-05-03 02:25:50.822673	2	f	\N	f	\N
43	1	2	2026-05-03 02:35:25.513099	Dolor torácico	ORANGE	YELLOW	En Espera	\N	\N	\N	t	2026-05-03 02:35:25.505507	2026-05-03 02:35:36.24054	2	f	\N	f	\N
44	1	2	2026-05-04 12:14:27.605068	Dolor torácico	ORANGE	RED	Llamado	\N	\N	\N	t	2026-05-04 12:14:27.582216	2026-05-04 12:30:41.615171	3	f	\N	f	\N
8	8	3	2026-05-02 14:15:00	Dificultad respiratoria	RED	RED	Atendido	Posible asma severo. Oxigenoterapia iniciada.	Gostrointeritis	166583	t	2026-05-02 14:15:00	2026-05-04 12:31:23.466602	4	f	\N	f	\N
45	53	2	2026-05-04 12:58:09.100138	Dolor torácico	RED	RED	En Espera	\N	\N	\N	t	2026-05-04 12:58:09.088439	2026-05-04 12:58:09.088439	1	f	\N	f	\N
46	54	2	2026-05-08 02:13:30.382922	Dolor torácico	RED	RED	En Espera	\N	\N	\N	t	2026-05-08 02:13:30.374175	2026-05-08 02:13:50.002283	2	f	\N	f	\N
\.


--
-- Data for Name: usuarios; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.usuarios (id, username, email, hashed_password, nombres, apellidos, rol, activo, last_login, created_at, updated_at, version) FROM stdin;
5	auditor1	auditor1@hospital.com	$2b$12$iQyRXDEHCt9kTqxfcMWgF.JOmX4g8B87XxLTPLIgHiobF.2qrXs8G	Patricia	Gonzalez	auditor	t	2026-05-03 08:26:47.931476	2026-05-03 00:02:55.239362	2026-05-03 03:26:47.620035	1
1	gerente1	gerente1@hospital.com	$2b$12$iQyRXDEHCt9kTqxfcMWgF.JOmX4g8B87XxLTPLIgHiobF.2qrXs8G	Carlos	Martinez	gerente	t	2026-05-04 17:37:04.315397	2026-05-03 00:02:55.239362	2026-05-04 12:37:03.972085	1
2	enfermera1	enfermera1@hospital.com	$2b$12$iQyRXDEHCt9kTqxfcMWgF.JOmX4g8B87XxLTPLIgHiobF.2qrXs8G	Maria	Lopez	enfermera	t	2026-05-08 07:03:42.944512	2026-05-03 00:02:55.239362	2026-05-08 02:03:42.576297	1
4	medico1	medico1@hospital.com	$2b$12$iQyRXDEHCt9kTqxfcMWgF.JOmX4g8B87XxLTPLIgHiobF.2qrXs8G	Juan	Perez	medico	t	2026-05-08 07:17:01.646729	2026-05-03 00:02:55.239362	2026-05-08 02:17:01.349398	1
3	enfermera2	enfermera2@hospital.com	$2b$12$iQyRXDEHCt9kTqxfcMWgF.JOmX4g8B87XxLTPLIgHiobF.2qrXs8G	Ana	Garcia	enfermera	t	2026-05-02 19:02:55.239362	2026-05-03 00:02:55.239362	2026-05-03 01:47:54.253989	1
6	medico2	medico2@hospital.com	$2b$12$iQyRXDEHCt9kTqxfcMWgF.JOmX4g8B87XxLTPLIgHiobF.2qrXs8G	Roberto	Sanchez	medico	t	2026-05-02 23:02:55.239362	2026-05-03 00:02:55.239362	2026-05-03 01:47:54.253989	1
7	enfermera3	enfermera3@hospital.com	$2b$12$iQyRXDEHCt9kTqxfcMWgF.JOmX4g8B87XxLTPLIgHiobF.2qrXs8G	Laura	Rodriguez	enfermera	t	2026-05-02 00:02:55.239362	2026-05-03 00:02:55.239362	2026-05-03 01:47:54.253989	1
8	medico3	medico3@hospital.com	$2b$12$iQyRXDEHCt9kTqxfcMWgF.JOmX4g8B87XxLTPLIgHiobF.2qrXs8G	Diego	Fernandez	medico	t	2026-05-02 21:02:55.239362	2026-05-03 00:02:55.239362	2026-05-03 01:47:54.253989	1
9	enfermera4	enfermera4@hospital.com	$2b$12$iQyRXDEHCt9kTqxfcMWgF.JOmX4g8B87XxLTPLIgHiobF.2qrXs8G	Carmen	Torres	enfermera	t	2026-05-02 14:02:55.239362	2026-05-03 00:02:55.239362	2026-05-03 01:47:54.253989	1
10	enfermera5	enfermera5@hospital.com	$2b$12$iQyRXDEHCt9kTqxfcMWgF.JOmX4g8B87XxLTPLIgHiobF.2qrXs8G	Sofia	Hernandez	enfermera	t	2026-05-02 20:02:55.239362	2026-05-03 00:02:55.239362	2026-05-03 01:47:54.253989	1
11	medico4	medico4@hospital.com	$2b$12$iQyRXDEHCt9kTqxfcMWgF.JOmX4g8B87XxLTPLIgHiobF.2qrXs8G	Alejandro	Ruiz	medico	t	2026-05-02 18:02:55.239362	2026-05-03 00:02:55.239362	2026-05-03 01:47:54.253989	1
12	enfermera6	enfermera6@hospital.com	$2b$12$iQyRXDEHCt9kTqxfcMWgF.JOmX4g8B87XxLTPLIgHiobF.2qrXs8G	Isabel	Rojas	enfermera	t	2026-05-02 16:02:55.239362	2026-05-03 00:02:55.239362	2026-05-03 01:47:54.253989	1
\.


--
-- Name: contactos_emergencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.contactos_emergencia_id_seq', 20, true);


--
-- Name: hce_antecedentes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hce_antecedentes_id_seq', 17, true);


--
-- Name: hce_consulta_previa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.hce_consulta_previa_id_seq', 10, true);


--
-- Name: logs_auditoria_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.logs_auditoria_id_seq', 37, true);


--
-- Name: pacientes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pacientes_id_seq', 54, true);


--
-- Name: resultados_ia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.resultados_ia_id_seq', 14, true);


--
-- Name: signos_vitales_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.signos_vitales_id_seq', 46, true);


--
-- Name: sintomas_triaje_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.sintomas_triaje_id_seq', 49, true);


--
-- Name: triajes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.triajes_id_seq', 46, true);


--
-- Name: usuarios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.usuarios_id_seq', 12, true);


--
-- Name: contactos_emergencia contactos_emergencia_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contactos_emergencia
    ADD CONSTRAINT contactos_emergencia_pkey PRIMARY KEY (id);


--
-- Name: hce_antecedentes hce_antecedentes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hce_antecedentes
    ADD CONSTRAINT hce_antecedentes_pkey PRIMARY KEY (id);


--
-- Name: hce_consulta_previa hce_consulta_previa_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hce_consulta_previa
    ADD CONSTRAINT hce_consulta_previa_pkey PRIMARY KEY (id);


--
-- Name: logs_auditoria logs_auditoria_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.logs_auditoria
    ADD CONSTRAINT logs_auditoria_pkey PRIMARY KEY (id);


--
-- Name: pacientes pacientes_dni_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_dni_key UNIQUE (dni);


--
-- Name: pacientes pacientes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pacientes
    ADD CONSTRAINT pacientes_pkey PRIMARY KEY (id);


--
-- Name: resultados_ia resultados_ia_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resultados_ia
    ADD CONSTRAINT resultados_ia_pkey PRIMARY KEY (id);


--
-- Name: resultados_ia resultados_ia_triaje_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resultados_ia
    ADD CONSTRAINT resultados_ia_triaje_id_key UNIQUE (triaje_id);


--
-- Name: signos_vitales signos_vitales_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos_vitales
    ADD CONSTRAINT signos_vitales_pkey PRIMARY KEY (id);


--
-- Name: signos_vitales signos_vitales_triaje_id_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos_vitales
    ADD CONSTRAINT signos_vitales_triaje_id_key UNIQUE (triaje_id);


--
-- Name: sintomas_triaje sintomas_triaje_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sintomas_triaje
    ADD CONSTRAINT sintomas_triaje_pkey PRIMARY KEY (id);


--
-- Name: triajes triajes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.triajes
    ADD CONSTRAINT triajes_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_email_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_email_key UNIQUE (email);


--
-- Name: usuarios usuarios_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id);


--
-- Name: usuarios usuarios_username_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_username_key UNIQUE (username);


--
-- Name: idx_logs_auditoria_modulo; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_logs_auditoria_modulo ON public.logs_auditoria USING btree (modulo, registro_id);


--
-- Name: idx_logs_auditoria_timestamp; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_logs_auditoria_timestamp ON public.logs_auditoria USING btree ("timestamp" DESC);


--
-- Name: idx_pacientes_dni; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pacientes_dni ON public.pacientes USING btree (dni) WHERE (activo = true);


--
-- Name: idx_pacientes_nombres; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_pacientes_nombres ON public.pacientes USING btree (nombres, apellidos);


--
-- Name: idx_sintomas_triaje_sintoma; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_sintomas_triaje_sintoma ON public.sintomas_triaje USING btree (sintoma);


--
-- Name: idx_triajes_estado_logistico; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_triajes_estado_logistico ON public.triajes USING btree (estado_logistico) WHERE (activo = true);


--
-- Name: idx_triajes_fecha_hora; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_triajes_fecha_hora ON public.triajes USING btree (fecha_hora DESC);


--
-- Name: idx_triajes_fecha_nivel; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_triajes_fecha_nivel ON public.triajes USING btree (fecha_hora, nivel_urgencia_final);


--
-- Name: idx_triajes_nivel_urgencia_final; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX idx_triajes_nivel_urgencia_final ON public.triajes USING btree (nivel_urgencia_final);


--
-- Name: pacientes update_pacientes_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER update_pacientes_updated_at BEFORE UPDATE ON public.pacientes FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: triajes update_triajes_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER update_triajes_updated_at BEFORE UPDATE ON public.triajes FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: usuarios update_usuarios_updated_at; Type: TRIGGER; Schema: public; Owner: -
--

CREATE TRIGGER update_usuarios_updated_at BEFORE UPDATE ON public.usuarios FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();


--
-- Name: contactos_emergencia contactos_emergencia_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contactos_emergencia
    ADD CONSTRAINT contactos_emergencia_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id) ON DELETE CASCADE;


--
-- Name: hce_antecedentes fk_antecedente_paciente; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hce_antecedentes
    ADD CONSTRAINT fk_antecedente_paciente FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id);


--
-- Name: hce_consulta_previa fk_consulta_paciente; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hce_consulta_previa
    ADD CONSTRAINT fk_consulta_paciente FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id);


--
-- Name: contactos_emergencia fk_contacto_paciente; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.contactos_emergencia
    ADD CONSTRAINT fk_contacto_paciente FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id);


--
-- Name: resultados_ia fk_resultados_ia_triaje; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resultados_ia
    ADD CONSTRAINT fk_resultados_ia_triaje FOREIGN KEY (triaje_id) REFERENCES public.triajes(id);


--
-- Name: signos_vitales fk_signos_triaje; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos_vitales
    ADD CONSTRAINT fk_signos_triaje FOREIGN KEY (triaje_id) REFERENCES public.triajes(id);


--
-- Name: sintomas_triaje fk_sintomas_triaje; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sintomas_triaje
    ADD CONSTRAINT fk_sintomas_triaje FOREIGN KEY (triaje_id) REFERENCES public.triajes(id);


--
-- Name: triajes fk_triaje_paciente; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.triajes
    ADD CONSTRAINT fk_triaje_paciente FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id);


--
-- Name: triajes fk_triaje_usuario; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.triajes
    ADD CONSTRAINT fk_triaje_usuario FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- Name: hce_antecedentes hce_antecedentes_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hce_antecedentes
    ADD CONSTRAINT hce_antecedentes_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id) ON DELETE CASCADE;


--
-- Name: hce_consulta_previa hce_consulta_previa_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.hce_consulta_previa
    ADD CONSTRAINT hce_consulta_previa_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id) ON DELETE CASCADE;


--
-- Name: logs_auditoria logs_auditoria_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.logs_auditoria
    ADD CONSTRAINT logs_auditoria_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id) ON DELETE SET NULL;


--
-- Name: resultados_ia resultados_ia_triaje_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resultados_ia
    ADD CONSTRAINT resultados_ia_triaje_id_fkey FOREIGN KEY (triaje_id) REFERENCES public.triajes(id) ON DELETE CASCADE;


--
-- Name: signos_vitales signos_vitales_triaje_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.signos_vitales
    ADD CONSTRAINT signos_vitales_triaje_id_fkey FOREIGN KEY (triaje_id) REFERENCES public.triajes(id) ON DELETE CASCADE;


--
-- Name: sintomas_triaje sintomas_triaje_triaje_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.sintomas_triaje
    ADD CONSTRAINT sintomas_triaje_triaje_id_fkey FOREIGN KEY (triaje_id) REFERENCES public.triajes(id) ON DELETE CASCADE;


--
-- Name: triajes triajes_paciente_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.triajes
    ADD CONSTRAINT triajes_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES public.pacientes(id);


--
-- Name: triajes triajes_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.triajes
    ADD CONSTRAINT triajes_usuario_id_fkey FOREIGN KEY (usuario_id) REFERENCES public.usuarios(id);


--
-- PostgreSQL database dump complete
--

\unrestrict dGoSDuDhf3R7Dhk9r3scXo9RoNWPl5UpjwiRcIpUzbiiavU8AYZrhsoYm5TIFcJ

