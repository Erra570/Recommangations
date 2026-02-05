--
-- PostgreSQL database dump
--

\restrict HFufNUHadzL39ziOfYq6Ic6s5k2okNhvuAzU5cb8aWCVH0NseUfQ4mcLochqFMe

-- Dumped from database version 16.11 (Debian 16.11-1.pgdg13+1)
-- Dumped by pg_dump version 16.11 (Debian 16.11-1.pgdg13+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO api;

--
-- Name: anime; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.anime (
    id integer NOT NULL,
    cover_image character varying,
    title_romaji character varying,
    title_english character varying,
    format character varying,
    start_date timestamp without time zone,
    country_of_origin character varying,
    mean_score double precision,
    dropped_paused integer,
    completed_watching integer,
    planning integer,
    variance_score double precision,
    status character varying,
    favourites integer,
    updated_at integer,
    episodes integer,
    is_adult boolean
);


ALTER TABLE public.anime OWNER TO api;

--
-- Name: anime_genres; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.anime_genres (
    anime_id integer NOT NULL,
    genre_id integer NOT NULL
);


ALTER TABLE public.anime_genres OWNER TO api;

--
-- Name: anime_id_seq; Type: SEQUENCE; Schema: public; Owner: api
--

CREATE SEQUENCE public.anime_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.anime_id_seq OWNER TO api;

--
-- Name: anime_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: api
--

ALTER SEQUENCE public.anime_id_seq OWNED BY public.anime.id;


--
-- Name: anime_staff; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.anime_staff (
    anime_id integer NOT NULL,
    staff_id integer NOT NULL,
    role character varying
);


ALTER TABLE public.anime_staff OWNER TO api;

--
-- Name: anime_studio; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.anime_studio (
    anime_id integer NOT NULL,
    studio_id integer NOT NULL
);


ALTER TABLE public.anime_studio OWNER TO api;

--
-- Name: anime_tags; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.anime_tags (
    anime_id integer NOT NULL,
    tag_id integer NOT NULL,
    is_spoiler boolean,
    rank integer
);


ALTER TABLE public.anime_tags OWNER TO api;

--
-- Name: genres; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.genres (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.genres OWNER TO api;

--
-- Name: genres_id_seq; Type: SEQUENCE; Schema: public; Owner: api
--

CREATE SEQUENCE public.genres_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.genres_id_seq OWNER TO api;

--
-- Name: genres_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: api
--

ALTER SEQUENCE public.genres_id_seq OWNED BY public.genres.id;


--
-- Name: manga; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.manga (
    id integer NOT NULL,
    cover_image character varying,
    title_romaji character varying,
    title_english character varying,
    format character varying,
    start_date timestamp without time zone,
    country_of_origin character varying,
    mean_score double precision,
    dropped_paused integer,
    completed_watching integer,
    planning integer,
    variance_score double precision,
    status character varying,
    favourites integer,
    updated_at integer,
    chapters integer,
    is_adult boolean
);


ALTER TABLE public.manga OWNER TO api;

--
-- Name: manga_genres; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.manga_genres (
    manga_id integer NOT NULL,
    genre_id integer NOT NULL
);


ALTER TABLE public.manga_genres OWNER TO api;

--
-- Name: manga_id_seq; Type: SEQUENCE; Schema: public; Owner: api
--

CREATE SEQUENCE public.manga_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.manga_id_seq OWNER TO api;

--
-- Name: manga_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: api
--

ALTER SEQUENCE public.manga_id_seq OWNED BY public.manga.id;


--
-- Name: manga_staff; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.manga_staff (
    manga_id integer NOT NULL,
    staff_id integer NOT NULL,
    role character varying
);


ALTER TABLE public.manga_staff OWNER TO api;

--
-- Name: manga_tags; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.manga_tags (
    manga_id integer NOT NULL,
    tag_id integer NOT NULL,
    is_spoiler boolean,
    rank integer
);


ALTER TABLE public.manga_tags OWNER TO api;

--
-- Name: staff; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.staff (
    id integer NOT NULL,
    name character varying
);


ALTER TABLE public.staff OWNER TO api;

--
-- Name: staff_id_seq; Type: SEQUENCE; Schema: public; Owner: api
--

CREATE SEQUENCE public.staff_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.staff_id_seq OWNER TO api;

--
-- Name: staff_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: api
--

ALTER SEQUENCE public.staff_id_seq OWNED BY public.staff.id;


--
-- Name: studio; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.studio (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.studio OWNER TO api;

--
-- Name: studio_id_seq; Type: SEQUENCE; Schema: public; Owner: api
--

CREATE SEQUENCE public.studio_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.studio_id_seq OWNER TO api;

--
-- Name: studio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: api
--

ALTER SEQUENCE public.studio_id_seq OWNED BY public.studio.id;


--
-- Name: tags; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.tags (
    id integer NOT NULL,
    name character varying NOT NULL,
    category character varying,
    is_spoiler boolean,
    is_adult boolean
);


ALTER TABLE public.tags OWNER TO api;

--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: api
--

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tags_id_seq OWNER TO api;

--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: api
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- Name: user_anime; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.user_anime (
    user_id integer NOT NULL,
    anime_id integer NOT NULL,
    status character varying,
    score double precision,
    progress integer,
    favourite boolean,
    repeat integer,
    last_watched timestamp without time zone
);


ALTER TABLE public.user_anime OWNER TO api;

--
-- Name: user_manga; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.user_manga (
    user_id integer NOT NULL,
    manga_id integer NOT NULL,
    status character varying,
    score double precision,
    progress integer,
    favourite boolean,
    repeat integer,
    last_read timestamp without time zone
);


ALTER TABLE public.user_manga OWNER TO api;

--
-- Name: users; Type: TABLE; Schema: public; Owner: api
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL
);


ALTER TABLE public.users OWNER TO api;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: api
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO api;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: api
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: anime id; Type: DEFAULT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime ALTER COLUMN id SET DEFAULT nextval('public.anime_id_seq'::regclass);


--
-- Name: genres id; Type: DEFAULT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.genres ALTER COLUMN id SET DEFAULT nextval('public.genres_id_seq'::regclass);


--
-- Name: manga id; Type: DEFAULT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.manga ALTER COLUMN id SET DEFAULT nextval('public.manga_id_seq'::regclass);


--
-- Name: staff id; Type: DEFAULT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.staff ALTER COLUMN id SET DEFAULT nextval('public.staff_id_seq'::regclass);


--
-- Name: studio id; Type: DEFAULT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.studio ALTER COLUMN id SET DEFAULT nextval('public.studio_id_seq'::regclass);


--
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.alembic_version (version_num) FROM stdin;
ad85f1a6b411
\.


--
-- Data for Name: anime; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.anime (id, cover_image, title_romaji, title_english, format, start_date, country_of_origin, mean_score, dropped_paused, completed_watching, planning, variance_score, status, favourites, updated_at, episodes, is_adult) FROM stdin;
1	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx1-GCsPm7waJ4kS.png	Cowboy Bebop	Cowboy Bebop	TV	1998-04-03 00:00:00	JP	86	35728	251306	138596	13	FINISHED	25900	1769527257	26	f
5	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx5-NozHwXWdNLCz.jpg	Cowboy Bebop: Tengoku no Tobira	Cowboy Bebop: The Movie - Knockin' on Heaven's Door	MOVIE	2001-09-01 00:00:00	JP	83	636	55626	21873	12	FINISHED	1407	1769527321	1	f
6	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx6-wd4saT1JzStH.jpg	TRIGUN	Trigun	TV	1998-04-01 00:00:00	JP	80	9964	83431	61209	14	FINISHED	5857	1769523713	26	f
7	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx7-6uh1fPvbgS9t.png	Witch Hunter ROBIN	Witch Hunter ROBIN	TV	2002-07-02 00:00:00	JP	69	1718	7772	12240	16	FINISHED	239	1769527274	26	f
8	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b8-ReS3TwSgrDDi.jpg	Bouken Ou Beet	Beet the Vandel Buster	TV	2004-09-30 00:00:00	JP	67	299	1424	1228	19	FINISHED	38	1769489108	52	f
15	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx15-A4F2t0TgWoi4.png	Eyeshield 21	Eyeshield 21	TV	2005-04-06 00:00:00	JP	76	4465	17139	10119	15	FINISHED	702	1769523772	145	f
16	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx16-S9k8qahNXoYP.jpg	Hachimitsu to Clover	Honey and Clover	TV	2005-04-15 00:00:00	JP	77	4862	17303	32847	16	FINISHED	860	1769527314	24	f
17	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx17-6kqIbdUk3dgi.png	Hungry Heart: Wild Striker	\N	TV	2002-09-11 00:00:00	JP	73	404	2700	1443	16	FINISHED	80	1769491465	52	f
18	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b18-r7IirVmwP89u.jpg	Initial D FOURTH STAGE	Initial D 4th Stage	TV	2004-04-17 00:00:00	JP	80	2007	34934	8358	13	FINISHED	852	1769527332	24	f
19	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx19-gtMC64182sm4.jpg	MONSTER	Monster	TV	2004-04-07 00:00:00	JP	88	29405	134701	134912	14	FINISHED	19889	1769527270	74	f
20	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx20-dE6UHbFFg1A5.jpg	NARUTO	Naruto	TV	2002-10-03 00:00:00	JP	81	48635	562955	41822	15	FINISHED	29766	1769527278	220	f
21	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx21-ELSYx3yMPcKM.jpg	ONE PIECE	ONE PIECE	TV	1999-10-20 00:00:00	JP	88	123584	450153	84864	16	RELEASING	91861	1769527254	\N	f
22	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx22-yEguU9EmxkjK.png	Tennis no Ouji-sama	The Prince of Tennis	TV	2001-10-10 00:00:00	JP	75	4670	17169	11746	16	FINISHED	676	1769527303	178	f
23	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx23-OwtP69d9B9kg.jpg	Ring ni Kakero 1	\N	TV	2004-10-06 00:00:00	JP	63	114	615	858	22	FINISHED	23	1769494746	12	f
24	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx24-FY8Y08LrROKE.png	School Rumble	School Rumble	TV	2004-10-05 00:00:00	JP	76	4409	27349	23720	15	FINISHED	1027	1769523740	26	f
25	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx25-H1etX7IgfFtQ.jpg	Sunabouzu	Desert Punk	TV	2004-10-06 00:00:00	JP	69	2743	10454	14141	18	FINISHED	338	1769512757	24	f
26	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx26-ADSztyHBNO39.jpg	TEXHNOLYZE	Texhnolyze	TV	2003-04-17 00:00:00	JP	77	5035	19786	51667	19	FINISHED	2617	1769523745	22	f
27	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx27-MOAaiBHHLfOY.png	Trinity Blood	Trinity Blood	TV	2005-04-29 00:00:00	JP	68	2212	12013	12457	17	FINISHED	1037	1769527301	24	f
28	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx28-QuKcZpUjTXzV.png	Yakitate!! Japan	\N	TV	2004-10-12 00:00:00	JP	76	1900	8210	8778	15	FINISHED	300	1769502040	69	f
29	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx29-0PsnJVadMG7k.jpg	Zipang	\N	TV	2004-10-07 00:00:00	JP	73	388	2202	3501	16	FINISHED	63	1769502040	26	f
30	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx30-AI1zr74Dh4ye.jpg	Shin Seiki Evangelion	Neon Genesis Evangelion	TV	1995-10-03 00:00:00	JP	84	22490	323473	95629	15	FINISHED	33315	1769527309	26	f
31	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx31-3zRThtzQH62E.png	Shin Seiki Evangelion Movie: Shi to Shinsei	Neon Genesis Evangelion: Death & Rebirth	MOVIE	1997-03-15 00:00:00	JP	74	632	43983	12334	17	FINISHED	547	1769488703	1	f
32	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx32-5JYsv0wc122I.jpg	Shin Seiki Evangelion Movie: Air / Magokoro wo, Kimi ni	Neon Genesis Evangelion: The End of Evangelion	MOVIE	1997-07-19 00:00:00	JP	86	1167	194818	31755	15	FINISHED	15354	1769527317	1	f
33	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx33-PSwfE5B0gejI.jpg	Kenpuu Denki Berserk	Berserk	TV	1997-10-07 00:00:00	JP	85	7877	97608	54555	14	FINISHED	9221	1769527278	25	f
43	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx43-Y6EjeEMM14dj.png	GHOST IN THE SHELL: Koukaku Kidoutai	Ghost in the Shell	MOVIE	1995-11-18 00:00:00	JP	81	1398	96135	59413	14	FINISHED	5779	1769527307	1	f
44	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx44-MG5I672UbWAy.png	Rurouni Kenshin: Meiji Kenkaku Romantan - Tsuioku-hen	Samurai X: Trust and Betrayal	OVA	1999-02-20 00:00:00	JP	85	732	26298	17544	13	FINISHED	1892	1769527344	4	f
45	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx45-DEFgZRCxiGmF.png	Rurouni Kenshin: Meiji Kenkaku Romantan	Rurouni Kenshin	TV	1996-01-10 00:00:00	JP	79	9468	42097	32332	14	FINISHED	2212	1769516348	94	f
46	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx46-Steq4sQpA6fq.png	Rurouni Kenshin: Meiji Kenkaku Romantan - Ishinshishi e no Requiem	Samurai X: The Motion Picture	MOVIE	1997-12-20 00:00:00	JP	72	151	5985	2437	16	FINISHED	48	1769487815	1	f
47	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx47-4CR68arv452h.jpg	AKIRA	Akira	MOVIE	1988-07-16 00:00:00	JP	80	2061	147471	60479	15	FINISHED	7022	1769527292	1	f
48	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx48-1Jxw9YoMf8LZ.png	.hack//SIGN	.hack//SIGN	TV	2002-04-04 00:00:00	JP	66	3649	16572	12418	19	FINISHED	537	1769523772	26	f
49	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx49-jv1G7rSP4lxg.png	Aa! Megami-sama!	Oh! My Goddess	OVA	1993-02-21 00:00:00	JP	70	396	6215	4492	16	FINISHED	116	1769523772	5	f
50	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx50-OdzAFLX6X6Hf.png	Aa! Megami-sama! (TV)	Oh! My Goddess (TV)	TV	2005-01-07 00:00:00	JP	70	2212	13043	8662	16	FINISHED	276	1769527344	24	f
51	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b51-qkm7PDhQr1jS.jpg	Tenshi Kinryouku	Angel Sanctuary	OVA	2000-05-25 00:00:00	JP	56	305	4127	2591	22	FINISHED	39	1769509105	3	f
52	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx52-i6aTXaa4w1QA.png	Kidou Tenshi Angelic Layer	Angelic Layer	TV	2001-04-01 00:00:00	JP	70	863	5375	4447	16	FINISHED	153	1769509105	26	f
53	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx53-GPDXGvbhg4w5.png	Ai Yori Aoshi	Ai Yori Aoshi	TV	2002-04-11 00:00:00	JP	67	1682	9004	6170	17	FINISHED	129	1769509105	24	f
54	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx54-NRZifY4de4u4.jpg	Appleseed (Movie)	Appleseed (Movie)	MOVIE	2004-04-17 00:00:00	JP	66	199	6968	3323	16	FINISHED	69	1769466072	1	f
55	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx55-uG26UwIxEJkJ.png	Arc the Lad	Arc the Lad	TV	1999-04-05 00:00:00	JP	62	271	1280	1374	17	FINISHED	19	1769487671	26	f
56	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b56-u0q9CHIgtbQG.jpg	Avenger	\N	TV	2003-10-02 00:00:00	JP	56	339	1482	1549	21	FINISHED	25	1769487671	13	f
57	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx57-4wTOlaVSgKoy.png	BECK	Beck: Mongolian Chop Squad	TV	2004-10-06 00:00:00	JP	81	4716	30175	40317	15	FINISHED	2488	1769520082	26	f
58	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b58-2KarB5N1dB0P.jpg	BLUE GENDER	Blue Gender	TV	1999-10-08 00:00:00	JP	66	1072	5536	9013	18	FINISHED	140	1769516348	26	f
59	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/nx59-0J95ZHgt4uyP.jpg	Chobits	Chobits	TV	2002-04-03 00:00:00	JP	71	6885	47955	28697	17	FINISHED	1606	1769527270	26	f
60	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx60-nWs0N9upSorj.png	Chrno Crusade	Chrono Crusade	TV	2003-11-24 00:00:00	JP	71	2781	15436	13247	17	FINISHED	346	1769487619	24	f
61	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/61.jpg	D.N.Angel	D.N.Angel	TV	2003-04-03 00:00:00	JP	67	1955	14123	5703	17	FINISHED	238	1769487603	26	f
62	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx62-llr25zE9LOm1.png	D.C.: Da Capo	D.C.~Da Capo~	TV	2003-07-05 00:00:00	JP	63	1198	6221	5398	19	FINISHED	74	1769491465	26	f
63	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx63-2EYTwbAK4CLR.jpg	DearS	DearS	TV	2004-07-11 00:00:00	JP	60	1497	14655	6402	19	FINISHED	186	1769488703	12	f
64	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx64-JsxXAcf3ZKo1.png	Rozen Maiden	Rozen Maiden	TV	2004-10-08 00:00:00	JP	71	2249	20173	13944	16	FINISHED	551	1769509105	12	f
65	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx65-SnVu0Txb00nV.jpg	Rozen Maiden: Träumend	Rozen Maiden: Dreaming	TV	2005-10-21 00:00:00	JP	73	594	12197	3429	15	FINISHED	164	1769498491	12	f
66	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx66-ZqYQWl6LsfeI.png	Azumanga Daiou THE ANIMATION	Azumanga Daioh	TV	2002-04-09 00:00:00	JP	80	8654	47141	41516	15	FINISHED	4052	1769527322	26	f
67	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/nx67-aBz3s2hBTtdH.jpg	Basilisk: Kouga Ninpouchou	Basilisk	TV	2005-04-13 00:00:00	JP	72	2183	12743	15855	17	FINISHED	396	1769523744	24	f
68	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx68-BY1vMbDYz977.jpg	Black Cat	Black Cat	TV	2005-10-06 00:00:00	JP	69	3321	22168	13315	16	FINISHED	1197	1769494746	23	f
69	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx69-OiowxBQs5McP.png	CLUSTER EDGE	\N	TV	2005-10-04 00:00:00	JP	57	231	658	1216	20	FINISHED	13	1769487536	25	f
71	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx71-Fi08vs7xNBMW.png	Full Metal Panic!	Full Metal Panic!	TV	2002-01-08 00:00:00	JP	72	6351	46843	33736	15	FINISHED	1102	1769527344	24	f
72	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx72-dalTPVFKaOuZ.png	Full Metal Panic? Fumoffu	Full Metal Panic? Fumoffu	TV	2003-08-26 00:00:00	JP	78	1373	31176	9838	14	FINISHED	758	1769523772	12	f
73	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx73-UgXDGEMBPGle.jpg	Full Metal Panic! The Second Raid	Full Metal Panic! The Second Raid	TV	2005-07-14 00:00:00	JP	77	941	28194	9773	13	FINISHED	466	1769498491	13	f
74	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b74-QZI9kO7eesrb.jpg	Gakuen Alice	\N	TV	2004-10-30 00:00:00	JP	74	944	10171	6027	16	FINISHED	468	1769527337	26	f
75	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx75-j5QtzskLdNry.jpg	Soukyuu no Fafner	Fafner	TV	2004-07-05 00:00:00	JP	70	1009	4766	7165	18	FINISHED	161	1769523702	25	f
76	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/nx76-wRwZobrx9MPj.jpg	Mahou Shoujo Lyrical Nanoha	Magical Girl Lyrical Nanoha	TV	2004-10-03 00:00:00	JP	72	1408	13491	11735	16	FINISHED	437	1769527344	13	f
77	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx77-SwBCj7R1enWi.png	Mahou Shoujo Lyrical Nanoha A's	Magical Girl Lyrical Nanoha A's	TV	2005-10-02 00:00:00	JP	79	442	10401	4078	14	FINISHED	369	1769527344	13	f
79	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/nx79-I1ODM0WcMlsn.jpg	SHUFFLE!	\N	TV	2005-07-08 00:00:00	JP	65	4039	25145	14646	18	FINISHED	336	1769527314	24	f
80	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx80-pdYJ12vSTmad.jpg	Kidou Senshi Gundam	Mobile Suit Gundam	TV	1979-04-07 00:00:00	JP	77	3564	25151	14563	14	FINISHED	1619	1769527320	43	f
81	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx81-qBgqd932d9lW.jpg	Kidou Senshi Gundam: Dai 08 MS Shotai	Mobile Suit Gundam: The 08th MS Team	OVA	1996-01-25 00:00:00	JP	77	748	15240	6066	14	FINISHED	597	1769527333	12	f
82	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx82-aw5fvnBOYuNw.png	Kidou Senshi Gundam 0080: Pocket no Naka no Sensou	Mobile Suit Gundam 0080: War in the Pocket	OVA	1989-03-25 00:00:00	JP	80	369	14345	5815	13	FINISHED	1161	1769512757	6	f
83	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx83-hMXIY88V9UDO.jpg	Kidou Senshi Gundam: Dai 08 MS Shotai - Miller's Report	Mobile Suit Gundam: The 08th MS Team - Miller's Report	MOVIE	1998-08-01 00:00:00	JP	64	96	2509	1043	15	FINISHED	14	1769487350	1	f
84	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx84-4wiZSMDFwFCN.jpg	Kidou Senshi Gundam 0083: STARDUST MEMORY	Mobile Suit Gundam 0083: Stardust Memory	OVA	1991-05-23 00:00:00	JP	68	473	9868	3612	17	FINISHED	162	1769516348	13	f
85	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx85-zdvoyoXDpjSs.jpg	Kidou Senshi Z Gundam	Mobile Suit Zeta Gundam	TV	1985-03-02 00:00:00	JP	79	1497	17591	6290	15	FINISHED	1585	1769527344	50	f
86	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b86-vaOa1TaV0T0K.png	Kidou Senshi Gundam Double Zeta	Mobile Suit Gundam ZZ	TV	1986-03-08 00:00:00	JP	66	884	11104	4238	18	FINISHED	341	1769527344	47	f
87	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx87-SCCIlaJZjSvz.png	Kidou Senshi Gundam: Gyakushuu no Char	Mobile Suit Gundam: Char's Counterattack	MOVIE	1988-03-12 00:00:00	JP	76	168	12610	3821	16	FINISHED	763	1769516348	1	f
88	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx88-A0p5JsI46tsX.png	Kidou Senshi Gundam F91	Mobile Suit Gundam F91	MOVIE	1991-03-16 00:00:00	JP	64	168	8025	2949	17	FINISHED	119	1769491465	1	f
89	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx89-835MY29WPRdm.jpg	Kidou Senshi Victory Gundam	Mobile Suit Victory Gundam	TV	1993-04-02 00:00:00	JP	67	660	5410	3641	20	FINISHED	193	1769523707	51	f
90	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b90-umBjF3yaeIdo.png	Shin Kidou Senki Gundam Wing	Mobile Suit Gundam Wing	TV	1995-04-07 00:00:00	JP	71	2341	19038	7972	17	FINISHED	624	1769523738	49	f
91	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx91-YkrzbtuWZThG.png	Shin Kidou Senki Gundam Wing: Endless Waltz	Mobile Suit Gundam Wing: Endless Waltz	OVA	1997-01-25 00:00:00	JP	73	154	6501	2041	16	FINISHED	88	1769487270	3	f
92	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx92-QICvHYE9HKyq.png	Kidou Shin Seiki Gundam X	After War Gundam X	TV	1996-04-05 00:00:00	JP	72	735	5871	3684	16	FINISHED	228	1769527344	39	f
93	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx93-pp8SI0zpA8EJ.jpg	Kidou Senshi Gundam SEED	Mobile Suit Gundam Seed	TV	2002-10-05 00:00:00	JP	73	1908	19677	7776	18	FINISHED	676	1769527338	50	f
94	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx94-tng83ksiXm5E.jpg	Kidou Senshi Gundam SEED DESTINY	Mobile Suit Gundam Seed Destiny	TV	2004-10-09 00:00:00	JP	66	922	13456	3643	21	FINISHED	267	1769520133	50	f
95	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/nx95-5okHk1B0VKro.jpg	∀ Gundam	Turn A Gundam	TV	1999-04-09 00:00:00	JP	81	1346	8412	9813	16	FINISHED	1258	1769527344	50	f
96	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx96-as1zJO34Qevb.png	Kidou Butouden G Gundam	Mobile Fighter G Gundam	TV	1994-04-22 00:00:00	JP	75	1243	10545	4897	17	FINISHED	674	1769516348	49	f
97	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/nx97-Loi1Ppy4quXy.jpg	Last Exile	Last Exile	TV	2003-04-07 00:00:00	JP	75	2035	12641	17821	15	FINISHED	453	1769527344	26	f
98	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx98-rGddbbtcCuYP.jpg	Mai-HiME	My-HiME	TV	2004-09-30 00:00:00	JP	70	1401	9334	9264	17	FINISHED	214	1769527344	26	f
99	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx99-NOVuOiWoqpMb.jpg	Mai-Otome	My-Otome	TV	2005-10-07 00:00:00	JP	70	479	4649	3119	18	FINISHED	95	1769487197	26	f
100	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx100-wr3vEOYOiAC1.png	Shin Shirayuki-hime Densetsu Pretear	Prétear: The New Legend of Snow White	TV	2001-04-04 00:00:00	JP	67	609	5344	4651	17	FINISHED	128	1769487191	13	f
101	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/nx101-x3YmfrzYZ9kM.jpg	AIR	Air	TV	2005-01-07 00:00:00	JP	69	2684	28513	17565	18	FINISHED	565	1769527344	13	f
102	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx102-nacpPTHmjvXJ.png	Aishiteruze Baby★★	Love You Baby	TV	2004-04-03 00:00:00	JP	72	1239	8409	4422	16	FINISHED	152	1769487150	26	f
103	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx103-v029gLfcQajN.jpg	Akazukin Chacha	Red Riding Hood Chacha	TV	1994-01-07 00:00:00	JP	72	402	1403	2355	19	FINISHED	79	1769487145	74	f
104	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx104-fUBucj3ywYzH.png	Ayashi no Ceres	Ceres, Celestial Legend	TV	2000-04-20 00:00:00	JP	66	737	3919	3934	19	FINISHED	79	1769502040	24	f
105	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/105.jpg	BOYS BE ...	\N	TV	2000-04-11 00:00:00	JP	60	374	1998	1863	19	FINISHED	17	1769487141	13	f
106	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/n106-KgEGNWhC9XLR.jpg	Hana Yori Dango	Hana Yori Dango (Boys Over Flowers)	TV	1996-09-08 00:00:00	JP	72	1064	5088	6616	20	FINISHED	252	1769527344	51	f
107	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx107-w685twC2xgyr.jpg	Ou Dorobou JING	Jing: King of Bandits	TV	2002-05-15 00:00:00	JP	67	536	2932	3484	18	FINISHED	59	1769487137	13	f
108	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/108.jpg	Ou Dorobou JING in Seventh Heaven	Jing: King of Bandits - Seventh Heaven	OVA	2004-01-21 00:00:00	JP	67	92	1302	951	16	FINISHED	12	1769385627	3	f
109	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx109-WfAppfDHUpBf.png	Bakuretsu Tenshi	Burst Angel	TV	2004-05-06 00:00:00	JP	64	1192	5302	5381	18	FINISHED	96	1769487133	24	f
110	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx110-KB2VJ8Qp3WD6.jpg	Chuuka Ichiban!	Cooking Master Boy	TV	1997-04-27 00:00:00	JP	72	359	1980	1899	15	FINISHED	51	1769517929	52	f
111	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx111-DxnHYJUnO4Dd.jpg	Corrector Yui	Corrector Yui	TV	1999-04-09 00:00:00	JP	68	440	2112	2566	18	FINISHED	100	1769523767	26	f
112	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/112.jpg	Chou Henshin Cosprayers	The Cosmopolitan Prayers	TV_SHORT	2004-01-12 00:00:00	JP	38	216	974	968	21	FINISHED	5	1769487121	8	f
113	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx113-LVBTWnBDpKb1.jpg	Uchuu no Stellvia	Stellvia of the Universe	TV	2003-04-03 00:00:00	JP	71	452	2504	3183	16	FINISHED	47	1769488703	26	f
114	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx114-VqL7lYKqdBR6.png	Sakigake!! Cromartie Koukou	Cromartie High School	TV_SHORT	2003-10-03 00:00:00	JP	76	3512	14767	15953	16	FINISHED	657	1769516348	26	f
115	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx115-tHn79Q8ITmBN.jpg	Ijigen no Sekai El Hazard	El Hazard: The Alternative World	TV	1998-01-08 00:00:00	JP	66	131	1116	946	18	FINISHED	15	1769448558	13	f
116	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx116-JdDCxwMpLRQV.png	Shinpi no Sekai El Hazard (TV)	El Hazard: The Wanderers	TV	1995-10-06 00:00:00	JP	68	277	1741	2086	18	FINISHED	43	1769487106	26	f
117	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx117-GUF1ulwYZWsk.png	Shinpi no Sekai El Hazard	El Hazard: The Magnificent World	OVA	1995-05-26 00:00:00	JP	70	238	2272	2638	16	FINISHED	43	1769512757	7	f
118	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/118.jpg	Shinpi no Sekai El Hazard 2	El Hazard 2: The Magnificent World	OVA	1997-03-21 00:00:00	JP	66	83	1202	742	18	FINISHED	11	1769378923	4	f
119	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx119-OitBgnCg8T7c.jpg	Final Approach	\N	TV_SHORT	2004-10-03 00:00:00	JP	60	356	3269	1820	18	FINISHED	26	1769487101	13	f
120	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx120-Z5i1sw1xboQP.jpg	Fruits Basket	Fruits Basket	TV	2001-07-05 00:00:00	JP	75	6064	55278	30809	17	FINISHED	1785	1769527336	26	f
121	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx121-zjmixZ428Mwv.png	Hagane no Renkinjutsushi	Fullmetal Alchemist	TV	2003-10-04 00:00:00	JP	79	17133	174788	49544	14	FINISHED	5961	1769523710	51	f
122	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx122-seEUpu2fDTtF.jpg	Full Moon wo Sagashite	Looking for the Full Moon	TV	2002-04-06 00:00:00	JP	77	1659	9251	9676	17	FINISHED	596	1769494746	52	f
123	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx123-nTVq4CHgK5Ly.jpg	Fushigi Yuugi	Fushigi Yugi: The Mysterious Play	TV	1995-04-06 00:00:00	JP	72	1804	8629	9405	18	FINISHED	415	1769527344	52	f
124	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/124.jpg	Fushigi Yuugi: Eikoden	Mysterious Play: Eikoden	OVA	2001-12-21 00:00:00	JP	62	95	1902	933	21	FINISHED	25	1769486976	4	f
125	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/125.jpg	Futakoi	Futakoi	TV	2004-10-06 00:00:00	JP	60	485	3343	2509	19	FINISHED	32	1769486974	13	f
126	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/126.jpg	Futakoi Alternative	Futakoi Alternative	TV	2005-04-07 00:00:00	JP	66	499	2654	3053	18	FINISHED	53	1769512757	13	f
127	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx127-gwP6xnzX1ZiY.png	Gate Keepers	Gate Keepers	TV	2000-04-03 00:00:00	JP	65	365	2023	1867	19	FINISHED	38	1769486969	24	f
128	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/128.jpg	Gate Keepers 21	\N	OVA	2002-04-24 00:00:00	JP	64	111	1117	844	18	FINISHED	19	1769486968	6	f
129	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx129-YjyAZNbmTGxE.png	Gensou Maden Saiyuuki	Saiyuki	TV	2000-04-04 00:00:00	JP	71	1000	4075	5025	17	FINISHED	149	1769527344	50	f
130	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx130-f0o2z5QN9qeO.png	Saiyuuki RELOAD	Saiyuki Reload	TV	2003-10-02 00:00:00	JP	70	377	2944	2640	17	FINISHED	56	1769494746	25	f
131	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/131.jpg	Saiyuuki RELOAD GUNLOCK	Saiyuki Gunlock	TV	2004-04-02 00:00:00	JP	69	187	1933	1799	17	FINISHED	20	1769486965	26	f
132	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx132-DBhi3KQASjLU.png	GetBackers: Dakkanya	GetBackers	TV	2002-10-05 00:00:00	JP	72	2070	8723	8071	16	FINISHED	256	1769498491	49	f
133	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx133-jsmCU1ZXlD7s.png	Green Green	Green Green	TV	2003-07-12 00:00:00	JP	54	1240	10095	4436	21	FINISHED	78	1769527330	12	f
134	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx134-f3dmmMOijYdn.png	GUNSLINGER GIRL	Gunslinger Girl	TV	2003-10-08 00:00:00	JP	74	2909	17930	19108	17	FINISHED	1270	1769527344	13	f
135	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx135-egPcTb3lAnbu.jpg	Hikaru no Go	Hikaru no Go	TV	2001-10-10 00:00:00	JP	79	2254	12499	11257	15	FINISHED	641	1769523772	75	f
136	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx136-gj0bbCpDNrKG.jpg	HUNTER×HUNTER	Hunter x Hunter	TV	1999-10-16 00:00:00	JP	83	9038	77076	35321	14	FINISHED	3473	1769527270	62	f
137	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx137-u17pWQRTZfKn.jpg	HUNTER×HUNTER OVA	Hunter x Hunter: Yorknew City	OVA	2002-01-17 00:00:00	JP	82	393	21466	6147	14	FINISHED	433	1769527344	8	f
138	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx138-BY6R1y8zuf7s.png	HUNTER×HUNTER: Greed Island	\N	OVA	2003-02-05 00:00:00	JP	80	435	25374	5360	15	FINISHED	297	1769502040	8	f
139	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx139-qiFhjx4o1sKI.png	HUNTER×HUNTER: Greed Island Final	\N	OVA	2004-03-03 00:00:00	JP	80	379	20537	4960	15	FINISHED	225	1769486827	14	f
141	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/141.jpg	Jinki:Extend	Jinki:Extend	TV	2005-01-05 00:00:00	JP	57	249	1179	1403	20	FINISHED	11	1769488703	12	f
142	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/nx142-gcfapg9oM7Qv.jpg	Kamikaze Kaitou Jeanne	\N	TV	1999-02-13 00:00:00	JP	72	668	5693	3997	17	FINISHED	237	1769488703	44	f
143	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx143-RcqeTmjW0Amu.jpg	Kannazuki no Miko	Destiny of the Shrine Maiden	TV	2004-10-02 00:00:00	JP	63	1047	7138	6854	20	FINISHED	190	1769491465	12	f
144	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx144-YdWsrDNssRIX.png	Kanon	\N	TV	2002-01-31 00:00:00	JP	65	791	6996	6630	19	FINISHED	93	1769486789	13	f
145	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx145-vcSv07afgy6c.png	Kareshi Kanojo no Jijou	His and Her Circumstances	TV	1998-10-02 00:00:00	JP	76	5017	22080	34907	15	FINISHED	1986	1769523717	26	f
146	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx146-JPwhcOFDs1bY.jpg	Kono Minikuku mo Utsukushii Sekai	This Ugly Yet Beautiful World	TV	2004-04-02 00:00:00	JP	62	757	5306	4118	19	FINISHED	47	1769486734	12	f
147	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx147-dK27Fk3dsn13.jpg	Kimi ga Nozomu Eien	Rumbling Hearts	TV	2003-10-05 00:00:00	JP	67	1367	12172	10195	19	FINISHED	223	1769520133	14	f
148	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx148-5Qvzc17vUOv0.png	Kita e.: Diamond Dust Drops	Diamond Daydreams	TV	2004-01-20 00:00:00	JP	64	183	835	1333	19	FINISHED	9	1769486715	12	f
149	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx149-6QGLHgJc8gum.png	LOVELESS	Loveless	TV	2005-04-07 00:00:00	JP	59	1606	9552	4843	22	FINISHED	124	1769502040	12	f
150	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx150-YRcwKiJEXcLx.png	BLOOD+	Blood+	TV	2005-10-08 00:00:00	JP	75	5426	27352	27208	18	FINISHED	2038	1769523744	50	f
151	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx151-QxUNuq82t7XK.jpg	Re: Cutie Honey	\N	OVA	2004-07-24 00:00:00	JP	71	510	6177	6013	16	FINISHED	284	1769509105	3	f
152	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx152-Dhq9vohv6AaN.jpg	Solty Rei	Solty Rei	TV	2005-10-06 00:00:00	JP	70	506	2640	2995	17	FINISHED	61	1769512757	24	f
153	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx153-pLhZPQCYk7hl.png	Juuni Kokuki	The Twelve Kingdoms	TV	2002-04-09 00:00:00	JP	78	2742	10446	23747	16	FINISHED	805	1769527344	45	f
154	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx154-hSYv4EtcBE1p.png	Shaman King	Shaman King	TV	2001-07-04 00:00:00	JP	74	4551	36426	15112	15	FINISHED	1095	1769527344	64	f
155	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx155-tDzea3RpxSZ8.jpg	X	\N	MOVIE	1996-08-03 00:00:00	JP	62	202	4742	4527	21	FINISHED	89	1769488703	1	f
156	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b156-MSqEz70iYng4.png	X (TV)	X (TV)	TV	2001-10-03 00:00:00	JP	69	1018	6396	8008	17	FINISHED	166	1769523729	24	f
157	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx157-huy9RpQkSH8c.png	Mahou Sensei Negima!	Negima!	TV	2005-01-06 00:00:00	JP	65	2223	14508	9124	17	FINISHED	199	1769523772	26	f
158	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx158-8bOVtlzJmq1r.jpg	Maria-sama ga Miteru	Maria Watches Over Us	TV	2004-01-08 00:00:00	JP	70	1104	5953	10887	17	FINISHED	202	1769527314	13	f
159	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/159.jpg	Boukyaku no Senritsu	Melody of Oblivion	TV	2004-04-07 00:00:00	JP	60	344	1344	2230	20	FINISHED	23	1769486492	24	f
160	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx160-t5rKPAhZoznO.jpg	Ima, Soko ni Iru Boku	Now and Then, Here and There	TV	1999-10-14 00:00:00	JP	73	1776	12846	25459	17	FINISHED	532	1769523772	13	f
161	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx161-oa4X4lL0KUO4.png	PEACE MAKER Kurogane	Peacemaker	TV	2003-10-08 00:00:00	JP	69	636	3913	4459	16	FINISHED	78	1769488703	24	f
162	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx162-mYmCcLeO1QQh.jpg	Pitaten	Pita-Ten	TV	2002-04-07 00:00:00	JP	66	430	2346	2019	18	FINISHED	48	1769527320	26	f
163	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b163-xg8mHh3R6o47.jpg	Power Stone	Power Stone	TV	1999-04-03 00:00:00	JP	63	191	1140	810	19	FINISHED	24	1769486458	26	f
164	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx164-ySuGzCWVw2cL.jpg	Mononoke-hime	Princess Mononoke	MOVIE	1997-07-12 00:00:00	JP	85	1520	220402	52888	13	FINISHED	11663	1769527269	1	f
165	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx165-TBPrUsYj4SUL.jpg	RahXephon	RahXephon	TV	2002-01-21 00:00:00	JP	71	1864	9670	15543	17	FINISHED	372	1769527314	26	f
166	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx166-aKHPMNS3oGQW.jpg	Samurai 7	Samurai 7	TV	2004-06-12 00:00:00	JP	71	1438	9883	9350	16	FINISHED	209	1769509105	26	f
167	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b167-qwMN7Wmlen5s.jpg	Scrapped Princess	Scrapped Princess	TV	2003-04-08 00:00:00	JP	71	1175	7337	9499	15	FINISHED	141	1769527344	24	f
168	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx168-kXxD2Cse752Y.png	Scryed	s-CRY-ed	TV	2001-07-04 00:00:00	JP	71	922	7364	6761	16	FINISHED	245	1769498491	26	f
169	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx169-ATwPxULRSDRr.jpg	Shingetsutan Tsukihime	Lunar Legend Tsukihime	TV	2003-10-10 00:00:00	JP	61	1962	15940	14902	21	FINISHED	253	1769520133	12	f
170	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx170-cmD8A0vZsp6g.jpg	SLAM DUNK	Slam Dunk	TV	1993-10-16 00:00:00	JP	83	6019	32068	28656	14	FINISHED	2776	1769527344	101	f
171	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx171-PKLAXt0u5vBb.png	Strange Dawn	\N	TV	2000-07-11 00:00:00	JP	64	178	803	1349	21	FINISHED	14	1769486203	13	f
173	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/173.jpg	tactics	\N	TV	2004-10-06 00:00:00	JP	68	560	2176	2739	17	FINISHED	41	1769486203	25	f
174	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx174-s2PpkrK9X3Rw.jpg	Tenjou Tenge	Tenjho Tenge	TV	2004-04-02 00:00:00	JP	64	2477	16261	11657	18	FINISHED	263	1769516348	24	f
175	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx175-ccHowbNQMcdm.png	Tokyo Underground	Tokyo Underground	TV	2002-04-02 00:00:00	JP	63	516	2490	2331	18	FINISHED	48	1769520133	26	f
176	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/176.jpg	Triangle Heart: Sweet Songs Forever	\N	OVA	2003-07-24 00:00:00	JP	55	97	974	887	18	FINISHED	5	1769486192	4	f
177	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx177-tU0wjdXRw5u8.png	Tsubasa Chronicle	Tsubasa RESERVoir CHRoNiCLE	TV	2005-04-09 00:00:00	JP	71	3226	16987	14920	17	FINISHED	419	1769527308	26	f
178	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b178-LhW1hq84JRHW.png	Ultra Maniac	Ultramaniac - Magical Girl	TV	2003-05-20 00:00:00	JP	70	529	2828	2695	17	FINISHED	66	1769486181	26	f
179	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/179.jpg	Tokimeki Fushigi Diary★Ultra Maniac	\N	SPECIAL	2002-08-06 00:00:00	JP	62	30	763	397	19	FINISHED	5	1769377683	1	f
180	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx180-67CAKcXsjpUt.png	Vandread	Vandread	TV	2000-10-03 00:00:00	JP	67	764	8278	5294	17	FINISHED	172	1769517929	13	f
181	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx181-MSG4LgXhyRhA.jpg	Vandread: the second stage	Vandread: The Second Stage	TV	2001-10-05 00:00:00	JP	71	221	5980	1519	16	FINISHED	99	1769486157	13	f
182	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx182-YzZtZWMZCSFf.png	Tenkuu no Escaflowne	Vision of Escaflowne	TV	1996-04-02 00:00:00	JP	74	2176	14796	19939	15	FINISHED	721	1769520092	26	f
183	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/183.jpg	Whistle!	\N	TV	2002-05-06 00:00:00	JP	70	242	1542	1082	17	FINISHED	37	1769486137	39	f
184	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b184-Th1H2ZfZvTnc.jpg	Xenosaga: THE ANIMATION	Xenosaga: The Animation	TV	2005-01-06 00:00:00	JP	59	349	1786	1669	20	FINISHED	32	1769486136	12	f
185	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b185-GvXiR8AKTmdn.jpg	Initial D	Initial D 1st Stage	TV	1998-04-19 00:00:00	JP	83	6148	64787	33631	13	FINISHED	5246	1769527344	26	f
186	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b186-eygBSoYwLCYt.jpg	Initial D SECOND STAGE	Initial D 2nd Stage	TV	1999-10-15 00:00:00	JP	81	888	45084	8326	12	FINISHED	976	1769527325	13	f
187	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/nx187-QyCAlBGY3EWw.jpg	Initial D THIRD STAGE	Initial D 3rd Stage	MOVIE	2001-01-13 00:00:00	JP	79	351	38393	7155	13	FINISHED	722	1769527344	1	f
188	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/188.jpg	Gosenzo San'e	Masquerade	OVA	1998-09-25 00:00:00	JP	57	50	382	380	22	FINISHED	7	1769488703	4	t
189	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx189-ybxKAazvr7cH.png	Love Hina	Love Hina	TV	2000-04-19 00:00:00	JP	67	3078	23762	14764	17	FINISHED	384	1769527344	24	f
190	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx190-oapgxvKLl3uW.png	Love Hina Again	Love Hina Again	OVA	2002-01-26 00:00:00	JP	68	219	9797	2429	17	FINISHED	56	1769486052	3	f
191	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx191-pKngFO6EOiqI.jpg	Love Hina Christmas Special: Silent Eve	Love Hina Christmas Movie	SPECIAL	2000-12-25 00:00:00	JP	69	112	6944	1273	16	FINISHED	44	1769486045	1	f
192	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx192-mEQSZUwiu2Na.jpg	Love Hina: Haru Special - Kimi Sakura Chiru Nakare!!	Love Hina Spring Movie	SPECIAL	2001-04-02 00:00:00	JP	68	108	6345	1301	17	FINISHED	32	1769486041	1	f
193	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/193.jpg	Maburaho	Maburaho	TV	2003-10-14 00:00:00	JP	62	1242	8825	4187	19	FINISHED	81	1769498491	24	f
194	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx194-WGTjEMUnjGaW.jpg	Macross Zero	Macross Zero	OVA	2002-12-21 00:00:00	JP	71	277	5735	4066	16	FINISHED	74	1769486030	5	f
195	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx195-0qMiRJbg60Tc.png	Onegai☆Teacher	Please☆Teacher!	TV	2002-01-10 00:00:00	JP	67	1405	18440	9256	18	FINISHED	320	1769527307	12	f
196	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/196.jpg	Onegai☆Twins	Please☆Twins!	TV	2003-07-15 00:00:00	JP	64	667	8896	3860	18	FINISHED	80	1769486018	12	f
197	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/197.jpg	Rizelmine	\N	TV_SHORT	2002-04-02 00:00:00	JP	60	543	2304	2065	20	FINISHED	37	1769520133	24	f
198	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx198-11hkVkT4h4Im.png	Speed Grapher	Speed Grapher	TV	2005-04-08 00:00:00	JP	69	1831	7738	13387	17	FINISHED	196	1769523743	24	f
199	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx199-sWefXJvXkDOb.jpg	Sen to Chihiro no Kamikakushi	Spirited Away	MOVIE	2001-07-20 00:00:00	JP	86	1614	385856	50103	13	FINISHED	17416	1769527331	1	f
200	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx200-xPxQtMoeRfyr.jpg	Tenshi na Konamaiki	\N	TV	2002-04-06 00:00:00	JP	71	630	2097	2867	18	FINISHED	48	1769502040	50	f
201	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx201-mrWfPJpsOwUH.jpg	Denei Shoujo VIDEO GIRL AI	Video Girl Ai	OVA	1992-03-27 00:00:00	JP	70	341	4084	4510	16	FINISHED	120	1769485820	6	f
202	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx202-w2OLL3j8WmDm.jpg	Wolf's Rain	Wolf's Rain	TV	2003-01-07 00:00:00	JP	75	3887	21888	30430	16	FINISHED	1083	1769523736	26	f
203	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b203-Vzy5DayEa7bp.jpg	Words Worth	Words Worth	OVA	1999-08-25 00:00:00	JP	60	114	847	626	20	FINISHED	19	1769485796	5	t
204	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/204.jpg	Yumeria	\N	TV	2004-01-09 00:00:00	JP	56	418	2307	1561	20	FINISHED	26	1769485795	12	f
205	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx205-7tHVFu6dPBm9.png	Samurai Champloo	Samurai Champloo	TV	2004-05-20 00:00:00	JP	84	18061	145978	90553	13	FINISHED	13360	1769527285	26	f
206	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx206-G9mTDCBNom5D.png	Lodoss-tou Senki: Eiyuu Kishi Den	Record of Lodoss War: Chronicles of the Heroic Knight	TV	1998-04-01 00:00:00	JP	68	465	2820	4603	17	FINISHED	68	1769485660	27	f
207	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx207-B2lxEFGigYgd.png	Lodoss-tou Senki	Record of Lodoss War	OVA	1990-06-30 00:00:00	JP	70	1432	9263	14832	16	FINISHED	431	1769527247	13	f
208	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx208-yOpLH6XOw2sc.jpg	R.O.D -READ OR DIE-	R.O.D - READ OR DIE	OVA	2001-05-23 00:00:00	JP	76	387	9867	7851	16	FINISHED	1031	1769488703	3	f
209	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx209-d0WO2JHIfzTu.png	R.O.D -THE TV-	R.O.D -THE TV-	TV	2003-09-01 00:00:00	JP	80	929	8023	6637	16	FINISHED	1427	1769523758	26	f
210	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx210-qgahLDYT0t9b.png	Ranma 1/2	Ranma ½	TV	1989-04-15 00:00:00	JP	76	7135	26376	17298	15	FINISHED	1311	1769527344	18	f
211	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/211.jpg	Pure Mail	\N	OVA	2001-09-25 00:00:00	JP	56	48	472	276	19	FINISHED	9	1769376636	2	t
212	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/nx212-SSB2S3cbIumn.jpg	Project A-Ko	Project A-ko	MOVIE	1986-06-21 00:00:00	JP	68	146	3930	4160	17	FINISHED	133	1769527284	1	f
213	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/213.jpg	Pia Carrot e Youkoso!!	Welcome to Pia Carrot	OVA	1997-10-24 00:00:00	JP	63	57	484	388	24	FINISHED	14	1769485511	3	t
214	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/214.jpg	Pia Carrot e Youkoso!! 2	Welcome To Pia Carrot 2	OVA	1998-10-23 00:00:00	JP	64	41	409	211	25	FINISHED	7	1769376632	3	t
215	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/215.jpg	Pia Carrot e Youkoso!! 2 DX	Welcome to Pia Carrot! 2 DX	OVA	1999-12-18 00:00:00	JP	61	66	533	370	22	FINISHED	9	1769485509	6	f
216	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/216.jpg	Pia Carrot e Youkoso!!: Sayaka no Koi Monogatari	Welcome to Pia Carrot! Sayaka's Love Story	MOVIE	2002-10-19 00:00:00	JP	58	59	531	347	22	FINISHED	2	1769376631	1	f
217	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/217.jpg	Shin Angel	New Angel	OVA	1994-10-21 00:00:00	JP	57	63	338	337	21	FINISHED	7	1769485507	5	t
218	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx218-qBfbgiJIR5rv.jpg	Kidou Senkan Nadesico	Martian Successor Nadesico	TV	1996-10-01 00:00:00	JP	74	1080	6271	8268	16	FINISHED	279	1769512757	26	f
219	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx219-zuElTO2hrJEZ.jpg	Kidou Senkan Nadesico: The prince of darkness	Martian Successor Nadesico: The Prince of Darkness	MOVIE	1998-08-01 00:00:00	JP	65	69	2770	1532	19	FINISHED	48	1769512757	1	f
220	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/b220-idJrGJWlOU0M.jpg	Kuro no Danshou	Mystery of the Necronomicon	OVA	1999-10-29 00:00:00	JP	47	54	268	220	21	FINISHED	5	1769376601	4	t
221	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx221-OIx9EYxmjTxB.png	Mezzo Forte	Mezzo Forte	OVA	2000-05-25 00:00:00	JP	65	177	5102	3944	18	FINISHED	112	1769527322	2	t
222	https://s4.anilist.co/file/anilistcdn/media/anime/cover/medium/bx222-AWGEcDS0VacZ.png	MEZZO	Mezzo	TV	2004-01-04 00:00:00	JP	63	379	2374	3461	18	FINISHED	55	1769512757	13	f
\.


--
-- Data for Name: anime_genres; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.anime_genres (anime_id, genre_id) FROM stdin;
\.


--
-- Data for Name: anime_staff; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.anime_staff (anime_id, staff_id, role) FROM stdin;
\.


--
-- Data for Name: anime_studio; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.anime_studio (anime_id, studio_id) FROM stdin;
\.


--
-- Data for Name: anime_tags; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.anime_tags (anime_id, tag_id, is_spoiler, rank) FROM stdin;
\.


--
-- Data for Name: genres; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.genres (id, name) FROM stdin;
\.


--
-- Data for Name: manga; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.manga (id, cover_image, title_romaji, title_english, format, start_date, country_of_origin, mean_score, dropped_paused, completed_watching, planning, variance_score, status, favourites, updated_at, chapters, is_adult) FROM stdin;
\.


--
-- Data for Name: manga_genres; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.manga_genres (manga_id, genre_id) FROM stdin;
\.


--
-- Data for Name: manga_staff; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.manga_staff (manga_id, staff_id, role) FROM stdin;
\.


--
-- Data for Name: manga_tags; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.manga_tags (manga_id, tag_id, is_spoiler, rank) FROM stdin;
\.


--
-- Data for Name: staff; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.staff (id, name) FROM stdin;
\.


--
-- Data for Name: studio; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.studio (id, name) FROM stdin;
\.


--
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.tags (id, name, category, is_spoiler, is_adult) FROM stdin;
\.


--
-- Data for Name: user_anime; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.user_anime (user_id, anime_id, status, score, progress, favourite, repeat, last_watched) FROM stdin;
\.


--
-- Data for Name: user_manga; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.user_manga (user_id, manga_id, status, score, progress, favourite, repeat, last_read) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: api
--

COPY public.users (id, username) FROM stdin;
\.


--
-- Name: anime_id_seq; Type: SEQUENCE SET; Schema: public; Owner: api
--

SELECT pg_catalog.setval('public.anime_id_seq', 1, false);


--
-- Name: genres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: api
--

SELECT pg_catalog.setval('public.genres_id_seq', 1, false);


--
-- Name: manga_id_seq; Type: SEQUENCE SET; Schema: public; Owner: api
--

SELECT pg_catalog.setval('public.manga_id_seq', 1, false);


--
-- Name: staff_id_seq; Type: SEQUENCE SET; Schema: public; Owner: api
--

SELECT pg_catalog.setval('public.staff_id_seq', 1, false);


--
-- Name: studio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: api
--

SELECT pg_catalog.setval('public.studio_id_seq', 1, false);


--
-- Name: tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: api
--

SELECT pg_catalog.setval('public.tags_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: api
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: anime_genres anime_genres_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime_genres
    ADD CONSTRAINT anime_genres_pkey PRIMARY KEY (anime_id, genre_id);


--
-- Name: anime anime_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime
    ADD CONSTRAINT anime_pkey PRIMARY KEY (id);


--
-- Name: anime_staff anime_staff_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime_staff
    ADD CONSTRAINT anime_staff_pkey PRIMARY KEY (anime_id, staff_id);


--
-- Name: anime_studio anime_studio_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime_studio
    ADD CONSTRAINT anime_studio_pkey PRIMARY KEY (anime_id, studio_id);


--
-- Name: anime_tags anime_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime_tags
    ADD CONSTRAINT anime_tags_pkey PRIMARY KEY (anime_id, tag_id);


--
-- Name: genres genres_name_key; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_name_key UNIQUE (name);


--
-- Name: genres genres_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.genres
    ADD CONSTRAINT genres_pkey PRIMARY KEY (id);


--
-- Name: manga_genres manga_genres_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.manga_genres
    ADD CONSTRAINT manga_genres_pkey PRIMARY KEY (manga_id, genre_id);


--
-- Name: manga manga_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.manga
    ADD CONSTRAINT manga_pkey PRIMARY KEY (id);


--
-- Name: manga_staff manga_staff_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.manga_staff
    ADD CONSTRAINT manga_staff_pkey PRIMARY KEY (manga_id, staff_id);


--
-- Name: manga_tags manga_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.manga_tags
    ADD CONSTRAINT manga_tags_pkey PRIMARY KEY (manga_id, tag_id);


--
-- Name: staff staff_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.staff
    ADD CONSTRAINT staff_pkey PRIMARY KEY (id);


--
-- Name: studio studio_name_key; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.studio
    ADD CONSTRAINT studio_name_key UNIQUE (name);


--
-- Name: studio studio_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.studio
    ADD CONSTRAINT studio_pkey PRIMARY KEY (id);


--
-- Name: tags tags_name_key; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_name_key UNIQUE (name);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: user_anime user_anime_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.user_anime
    ADD CONSTRAINT user_anime_pkey PRIMARY KEY (user_id, anime_id);


--
-- Name: user_manga user_manga_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.user_manga
    ADD CONSTRAINT user_manga_pkey PRIMARY KEY (user_id, manga_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: ix_anime_id; Type: INDEX; Schema: public; Owner: api
--

CREATE INDEX ix_anime_id ON public.anime USING btree (id);


--
-- Name: ix_manga_id; Type: INDEX; Schema: public; Owner: api
--

CREATE INDEX ix_manga_id ON public.manga USING btree (id);


--
-- Name: ix_users_id; Type: INDEX; Schema: public; Owner: api
--

CREATE INDEX ix_users_id ON public.users USING btree (id);


--
-- Name: anime_genres anime_genres_anime_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime_genres
    ADD CONSTRAINT anime_genres_anime_id_fkey FOREIGN KEY (anime_id) REFERENCES public.anime(id);


--
-- Name: anime_genres anime_genres_genre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime_genres
    ADD CONSTRAINT anime_genres_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES public.genres(id);


--
-- Name: anime_staff anime_staff_anime_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime_staff
    ADD CONSTRAINT anime_staff_anime_id_fkey FOREIGN KEY (anime_id) REFERENCES public.anime(id);


--
-- Name: anime_staff anime_staff_staff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime_staff
    ADD CONSTRAINT anime_staff_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staff(id);


--
-- Name: anime_studio anime_studio_anime_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime_studio
    ADD CONSTRAINT anime_studio_anime_id_fkey FOREIGN KEY (anime_id) REFERENCES public.anime(id);


--
-- Name: anime_studio anime_studio_studio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime_studio
    ADD CONSTRAINT anime_studio_studio_id_fkey FOREIGN KEY (studio_id) REFERENCES public.studio(id);


--
-- Name: anime_tags anime_tags_anime_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime_tags
    ADD CONSTRAINT anime_tags_anime_id_fkey FOREIGN KEY (anime_id) REFERENCES public.anime(id);


--
-- Name: anime_tags anime_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.anime_tags
    ADD CONSTRAINT anime_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id);


--
-- Name: manga_genres manga_genres_genre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.manga_genres
    ADD CONSTRAINT manga_genres_genre_id_fkey FOREIGN KEY (genre_id) REFERENCES public.genres(id);


--
-- Name: manga_genres manga_genres_manga_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.manga_genres
    ADD CONSTRAINT manga_genres_manga_id_fkey FOREIGN KEY (manga_id) REFERENCES public.manga(id);


--
-- Name: manga_staff manga_staff_manga_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.manga_staff
    ADD CONSTRAINT manga_staff_manga_id_fkey FOREIGN KEY (manga_id) REFERENCES public.manga(id);


--
-- Name: manga_staff manga_staff_staff_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.manga_staff
    ADD CONSTRAINT manga_staff_staff_id_fkey FOREIGN KEY (staff_id) REFERENCES public.staff(id);


--
-- Name: manga_tags manga_tags_manga_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.manga_tags
    ADD CONSTRAINT manga_tags_manga_id_fkey FOREIGN KEY (manga_id) REFERENCES public.manga(id);


--
-- Name: manga_tags manga_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.manga_tags
    ADD CONSTRAINT manga_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id);


--
-- Name: user_anime user_anime_anime_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.user_anime
    ADD CONSTRAINT user_anime_anime_id_fkey FOREIGN KEY (anime_id) REFERENCES public.anime(id);


--
-- Name: user_anime user_anime_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.user_anime
    ADD CONSTRAINT user_anime_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: user_manga user_manga_manga_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.user_manga
    ADD CONSTRAINT user_manga_manga_id_fkey FOREIGN KEY (manga_id) REFERENCES public.manga(id);


--
-- Name: user_manga user_manga_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: api
--

ALTER TABLE ONLY public.user_manga
    ADD CONSTRAINT user_manga_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict HFufNUHadzL39ziOfYq6Ic6s5k2okNhvuAzU5cb8aWCVH0NseUfQ4mcLochqFMe

