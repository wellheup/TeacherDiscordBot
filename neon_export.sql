--
-- PostgreSQL database dump
--

\restrict 9vjkKWaBUykxlYshpaHFZpW1omnczpC59fMOpeFOBEPw9baTlAFzUQTaOk6xPFj

-- Dumped from database version 16.12 (ed61a14)
-- Dumped by pg_dump version 16.10

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
-- Name: app_config; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.app_config (
    key character varying NOT NULL,
    value character varying
);


ALTER TABLE public.app_config OWNER TO neondb_owner;

--
-- Name: assignments; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.assignments (
    assignment_id integer NOT NULL,
    description character varying,
    date_added date
);


ALTER TABLE public.assignments OWNER TO neondb_owner;

--
-- Name: assignments_assignment_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.assignments_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.assignments_assignment_id_seq OWNER TO neondb_owner;

--
-- Name: assignments_assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.assignments_assignment_id_seq OWNED BY public.assignments.assignment_id;


--
-- Name: bugs; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.bugs (
    bug_id integer NOT NULL,
    description text NOT NULL,
    added_by character varying(255) NOT NULL
);


ALTER TABLE public.bugs OWNER TO neondb_owner;

--
-- Name: bugs_bug_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.bugs_bug_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.bugs_bug_id_seq OWNER TO neondb_owner;

--
-- Name: bugs_bug_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.bugs_bug_id_seq OWNED BY public.bugs.bug_id;


--
-- Name: demo_assignments; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.demo_assignments (
    assignment_id integer NOT NULL,
    description character varying,
    date_added date
);


ALTER TABLE public.demo_assignments OWNER TO neondb_owner;

--
-- Name: demo_assignments_assignment_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.demo_assignments_assignment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.demo_assignments_assignment_id_seq OWNER TO neondb_owner;

--
-- Name: demo_assignments_assignment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.demo_assignments_assignment_id_seq OWNED BY public.demo_assignments.assignment_id;


--
-- Name: demo_bugs; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.demo_bugs (
    description text,
    added_by character varying(255),
    bug_id bigint NOT NULL
);


ALTER TABLE public.demo_bugs OWNER TO neondb_owner;

--
-- Name: demo_bugs_bug_id_temp_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.demo_bugs_bug_id_temp_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.demo_bugs_bug_id_temp_seq OWNER TO neondb_owner;

--
-- Name: demo_bugs_bug_id_temp_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.demo_bugs_bug_id_temp_seq OWNED BY public.demo_bugs.bug_id;


--
-- Name: demo_syllabus; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.demo_syllabus (
    book character varying(200),
    author character varying(200),
    series character varying(200),
    is_completed boolean,
    added_by character varying(200),
    season integer,
    num_in_series integer,
    is_extra_credit boolean,
    date_completed date,
    up_votes integer,
    date_added date,
    genre character varying(200),
    down_votes integer,
    unique_id bigint NOT NULL
);


ALTER TABLE public.demo_syllabus OWNER TO neondb_owner;

--
-- Name: demo_syllabus_unique_id_temp_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.demo_syllabus_unique_id_temp_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.demo_syllabus_unique_id_temp_seq OWNER TO neondb_owner;

--
-- Name: demo_syllabus_unique_id_temp_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.demo_syllabus_unique_id_temp_seq OWNED BY public.demo_syllabus.unique_id;


--
-- Name: syllabus; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.syllabus (
    book character varying(200),
    author character varying(200),
    series character varying(200),
    is_completed boolean DEFAULT false,
    added_by character varying(200),
    season integer,
    num_in_series integer,
    is_extra_credit boolean,
    date_completed date,
    up_votes integer DEFAULT 0,
    date_added date,
    genre character varying(200),
    unique_id integer NOT NULL,
    down_votes integer DEFAULT 0
);


ALTER TABLE public.syllabus OWNER TO neondb_owner;

--
-- Name: syllabus_newuniqueid_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.syllabus_newuniqueid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.syllabus_newuniqueid_seq OWNER TO neondb_owner;

--
-- Name: syllabus_newuniqueid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.syllabus_newuniqueid_seq OWNED BY public.syllabus.unique_id;


--
-- Name: assignments assignment_id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.assignments ALTER COLUMN assignment_id SET DEFAULT nextval('public.assignments_assignment_id_seq'::regclass);


--
-- Name: bugs bug_id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.bugs ALTER COLUMN bug_id SET DEFAULT nextval('public.bugs_bug_id_seq'::regclass);


--
-- Name: demo_assignments assignment_id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.demo_assignments ALTER COLUMN assignment_id SET DEFAULT nextval('public.demo_assignments_assignment_id_seq'::regclass);


--
-- Name: demo_bugs bug_id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.demo_bugs ALTER COLUMN bug_id SET DEFAULT nextval('public.demo_bugs_bug_id_temp_seq'::regclass);


--
-- Name: demo_syllabus unique_id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.demo_syllabus ALTER COLUMN unique_id SET DEFAULT nextval('public.demo_syllabus_unique_id_temp_seq'::regclass);


--
-- Name: syllabus unique_id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.syllabus ALTER COLUMN unique_id SET DEFAULT nextval('public.syllabus_newuniqueid_seq'::regclass);


--
-- Data for Name: app_config; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.app_config (key, value) FROM stdin;
last_update	2026-04-10
url_suffix	1t33bjve
\.


--
-- Data for Name: assignments; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.assignments (assignment_id, description, date_added) FROM stdin;
1	test	2024-06-11
2	test3	2024-06-11
3	Read up to Ch. 6 (part 1) of Black Leopard Red Wolf by June 17th	2024-06-11
4	Read up to Ch. 9 (but not including) of Black Leopard Red Wolf by July 1	2024-06-21
5	Read up to Ch. 14 (but not including) of Black Leopard Red Wolf by July 15	2024-07-02
6	Read up to Ch. 14 (but not including) of Black Leopard Red Wolf by July 15, assigned on 2024-07-02	2024-07-02
7	Read up to Ch. 14 (but not including) of Black Leopard Red Wolf by July 15, assigned on 2024-07-02	2024-07-02
8	Read up to but not including Ch 18 of Black Leopard Red Wolf by July 29	2024-07-16
9	Read	2024-07-30
10	Read up to but not including Ch 22 of Black Leopard Red Wolf by August 12	2024-07-30
11	Read to the end of Black Leopard Red Wolf by August  26th	2024-08-13
12	Read	2024-08-27
13	Read up to Ch 3 (but not Ch 3) of Annihilation by 9/9	2024-08-27
14	Finish Annihilation by 9/23	2024-09-10
15	Think patiently about books until we know what book to read next. 	2024-09-24
16	Read up to Ch. 12 of Iron Flame by 10/14\nRead up to Ch 7 of Authority by 10/7	2024-09-24
17	Read up to Ch. 12 of Iron Flame by 10/21?\nRead up to Ch 7 of Authority by 10/28?	2024-10-15
18	Read up to Ch 21 of Iron Flame by Nov 4?	2024-10-22
19	Read up to Ch 21 of Iron Flame by Nov 4 & Read up to Hauntings of Authority by Nov 11	2024-10-29
20	Read up to Hauntings of Authority by Nov 11 & Read up to Ch 35 of Iron Flame by Nov 18	2024-11-05
21	Read up to Hauntings of Authority by Nov 11 & Read up to Ch 35 of Iron Flame by Nov 18	2024-11-05
22	Read up to Ch 21 of Iron Flame by Nov 18 & Read up to the end of Authority by Nov 25	2024-11-12
23	Read up to Ch 35 of Iron Flame by Nov 18 & Read up to the end of Authority by Nov 25	2024-11-13
24	Read up to Ch 21 of Iron Flame by Nov 21 & Read up to the end of Authority by Nov 25	2024-11-19
25	Read up to Ch 35 of Iron Flame by Nov 21 & Read up to the end of Authority by Nov 25	2024-11-19
26	Read up to Ch 43 of Iron Flame by Dec 2 & Read up to the end of Authority by Nov 25	2024-11-22
28	Read up to Ch 43 of Iron Flame by Dec 2 & Read up to Ch 8 of Acceptance by Dec 9	2024-11-26
27	Read up to Ch 43 of Iron Flame by Dec 2 & Read up to Ch 8 of Acceptance by Dec 9	2024-11-26
29	Read up to Ch 54 by Dec 16 & Read up to Ch 8 of Acceptance by Dec 9	2024-12-03
30	Read up to Ch 54 of Iron Flame by Dec 16 & Read up to Ch 8 of Acceptance by Dec 9	2024-12-04
31	Read up to Ch 54 of Iron Flame by Dec 16 & Read up to Ch 14 of Acceptance by Dec 23	2024-12-10
32	Read up to Ch 54 of Iron Flame by Dec 16 & Read up to Ch 14 of Acceptance by Dec 23	2024-12-10
33	Finish Iron Flame by Jan 13 & Read up to Ch 14 of Acceptance by Jan 6	2024-12-31
34	Finish Iron Flame by Jan 13 & Finish Acceptance by Jan 20	2025-01-07
35	The	2025-01-21
36	The Poppy War Read up to and not including Chapter 6 by Feb 3rd	2025-01-21
37	The Poppy War Read up to and not including Chapter 10 by Feb 17th	2025-02-04
38	read The Poppy War up to but not including Chapter 15 by March 3rd	2025-02-18
39	read The Poppy War up to but not including Chapter 22 by March 17th	2025-03-07
40	Finish The Poppy War before we finish the month!	2025-03-18
41	read all of A Psalm for the Wild-Built by April 21st	2025-04-01
42	Read Iron Widow, up to and not including Chapter 11	2025-04-22
43	Read Iron Widow, up to and not including Chapter 11 by May 12	2025-04-22
44	Read Iron Widow, up to and not including Chapter 24 by May 26	2025-05-13
45	Read Iron Widow, up to and not including Chapter 37 by June 9th	2025-05-27
46	Read the rest of Iron Widow by June 23rd	2025-06-10
47	Get Emily Wilde's Encyclopedia of Faeries and read up to and not including '12th November' by July 14th	2025-06-24
48	Read up to and not including 26th November-Late by 7/28	2025-07-15
49	Finish	2025-07-29
50	Finish Emily Wilde's Encyclopaedia of Faeries by Aug 11th	2025-07-29
51	Finish	2025-07-29
52	Finish Emily Wilde's Encyclopaedia of Faeries and Even Though I Knew The End by Sept 1st	2025-07-29
53	The new assignment is: Finish Emily Wilde's Encyclopaedia of Faeries and Even Though I Knew The End by Sept 1st (for SUPER book club)	2025-07-29
54	The new assignment is: Finish Emily Wilde's Encyclopaedia of Faeries by August 14th and read Even Though I Knew The End by Sept 1st	2025-07-29
55	The new assignment is: Finish Emily Wilde's Encyclopaedia of Faeries by August 11th and read Even Though I Knew The End by Sept 1st	2025-08-11
56	Buy and read Even Though I Knew The End by Sept 1st	2025-08-12
57	Read up to (but not including) Ch. 7 of Moon Witch Spider King	2025-09-02
58	Read up to (but not including) Ch. 7 of Moon Witch Spider King	2025-09-02
59	Read up to Ch. 7 of Moon Witch Spider King by 9/15	2025-09-02
61	Read up to Part 2 of Moon Witch Spider King by October 6th	2025-09-22
64	Read	2025-10-07
65	Read part 2 of Moon Witch Spider King by Oct 20	2025-10-07
66	Read part 3 of Moon Witch Spider King by November 3	2025-10-21
67	Finish Moon Witch, Spider King by Nov 17th	2025-11-04
68	Acquire and read all of the A Prayer for the Crown-Shy by Decemeber 8th	2025-11-18
69	Acquire	2025-12-09
70	Acquire and read Part ??? by December 22nd	2025-12-09
71	Acquire and read Part ??? of Emily Wilde's Map of the Otherlands by December 22nd	2025-12-09
72	Acquire and read Part ??? of Emily Wilde's Map of the Otherlands up to and not including 'September 24th' by December 22nd	2025-12-09
73	Acquire and read up to and not including 'September 24th' of Emily Wilde's Map of the Otherlands by December 22nd	2025-12-09
74	Acquire and read up to and not including 'October 8th' of Emily Wilde's Map of the Otherlands by January 5th	2025-12-23
75	Read up to and not including 'October 8th' of Emily Wilde's Map of the Otherlands by January 5th	2025-12-23
76	Read up to and not including  '8th October' of Emily Wilde's Map of the Otherlands by 5th January	2025-12-23
77	Read the remainder of Emily Wilde's Map of the Otherlands by January 19th	2026-01-06
78	Get and read the first 200ish pages of Dungeon Crawler Carl by 2/9	2026-01-20
79	Get and read the first 100-ish pages of Dungeon Crawler Carl by Matt Dinniman by Feb 9th.	2026-01-20
80	Acquire Dungeon Crawler Carl and read up to but not including Ch 12 by Feb 9th	2026-02-03
81	Read Dungeon Crawler Carl up to but not including Ch 31 by Feb 23th	2026-02-10
82	Finish Dungeon Crawler Carl by March 9th	2026-02-24
83	Read Silver Under Nightfall up to but not including chapter 9 by March 23rd	2026-03-10
84	Read Silver Under Nightfall up to but not including chapter 24 by April 6th	2026-03-24
85	Finish Silver Under Nightfall by April 20th	2026-04-07
\.


--
-- Data for Name: bugs; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.bugs (bug_id, description, added_by) FROM stdin;
15	add a feature to determine who gets to choose the next book, who chose the last, and who has chosen how many, also a randomizer for who is next in the case of a tie	Phil
16	add a feature to add a table for each book and then keep a list of or character fan-cast ideas for each book?	Phil
17	add a command to print all of the books in a season	Phil
18	add a command to print all of the seasons and their books in the order the seasons occurred	Phil
19	upgrade to use gunicorn instead of flask?	Phil
20	add a WSDL page for the website	anonymous
29	make teacher check for a pinned post in office-hours channel when it updates the daily URL, if that pinned link exists, update that link	phil
35	create a selenium and cypress based repls to test automation frameworks	phil
37	add a Done counter to the top of Syllabus page to track who has finished reading	Phil
49	fix the hidden bug where forms try to submit extra times	Phil
55	Add links to each series to popup and show all books in the series	phil
56	Add time completed to pytest automation	Phil
57	add dockerized cypress testing  and time completed to unit tests tab	Phil
58	update the cypress front end automation with best practices including API calls to prep each test ahead of time	Phil
59	you can't undo a "completed on"	phil
\.


--
-- Data for Name: demo_assignments; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.demo_assignments (assignment_id, description, date_added) FROM stdin;
1	bar	2024-06-11
2	do some stuff	2024-06-21
3	temp	2024-07-02
4	Read a got dang book	2024-07-19
5	Read a got dang book	2024-07-19
6	Read a got dang book	2024-07-19
7	Read a got dang book	2024-07-19
8	\N	2024-07-19
9	Read a got dang book	2024-07-19
10	a whole new assignment	2024-08-01
11	KILL THE BATMAN	2024-08-09
12	Read up to but not including Ch 22 of Black Leopard Red Wolf by August 12, assigned on 2024-07-30	2024-08-09
13	eat a whole bagel	2024-08-11
14	soup baby!	2024-08-11
15	Read a got dang book	2024-08-11
16	words	2024-08-11
17	a whole new assignment	2024-08-11
18	eat a whole bagel	2024-08-11
19	words	2024-08-11
20	words	2024-08-11
21	Read a got dang book	2024-08-11
22	eat a whole bagel	2024-08-11
23	Please. Control yourself.	2024-08-12
24	Get it together.	2024-08-12
25	let it all fall apart	2024-08-12
26	Read Chapter 5	2024-08-20
27	Read Chapter 5	2024-08-20
28	Read Chapter 5	2024-08-20
29	Read Chapter 5	2024-08-20
30	Read Chapter 5	2024-08-20
31	Read Chapter 5	2024-08-20
32	Read Chapter 5	2024-08-20
33	Read Chapter 5	2024-08-20
34	Read Chapter 5	2024-08-20
35	Read Chapter 5	2024-08-20
36	Read Chapter 5	2024-08-20
37	Read Chapter 5	2024-08-20
38	Read Chapter 5	2024-08-20
39	Read Chapter 5	2024-08-20
40	Read Chapter 5	2024-08-20
41	Read Chapter 5	2024-08-20
42	Read Chapter 5	2024-08-20
43	Read Chapter 5	2024-08-20
44	Read Chapter 5	2024-08-20
45	Read Chapter 5	2024-08-20
46	Read Chapter 5	2024-08-20
47	Read Chapter 5	2024-08-20
48	Read Chapter 5	2024-08-20
49	Read Chapter 5	2024-08-20
50	Read Chapter 5	2024-08-20
51	Read Chapter 5	2024-08-20
52	Read Chapter 5	2024-08-20
53	Read Chapter 5	2024-08-20
54	Read Chapter 5	2024-08-20
55	Read Chapter 5	2024-08-20
56	Read Chapter 5	2024-08-20
57	Read Chapter 5	2024-08-20
58	Read Chapter 5	2024-08-20
59	Read Chapter 5	2024-08-20
60	Read Chapter 5	2024-08-21
61	Read Chapter 5	2024-08-21
62	Read Chapter 5	2024-08-21
63	Read Chapter 5	2024-08-21
64	Read Chapter 5	2024-08-21
65	Read Chapter 5	2024-08-21
66	Read Chapter 5	2024-08-21
67	Read Chapter 5	2024-08-21
68	Read Chapter 5	2024-08-21
69	Read Chapter 5	2024-08-21
70	Read Chapter 5	2024-08-21
71	Read Chapter 5	2024-08-21
72	Read Chapter 5	2024-08-21
73	Read Chapter 5	2024-08-21
74	words	2024-08-25
75	words	2024-08-25
76	Read a got dang book	2024-08-25
77	Read a got dang book	2024-08-25
78	Read a got dang book	2024-08-25
80	fart for fun	2024-08-26
81	fart for fun	2024-08-26
79	fart for fun	2024-08-26
82	fart for fun	2024-08-26
83	fart for fun	2024-08-26
84	fart for fun	2024-08-26
85	fart for fun	2024-08-26
86	fart for fun	2024-08-26
87	fart for fun	2024-08-26
88	dream	2024-08-26
90	words	2024-08-26
89	words	2024-08-26
91	words	2024-08-26
92	words	2024-08-26
93	words	2024-08-26
94	words	2024-08-26
95	words	2024-08-26
96	words	2024-08-26
97	words	2024-08-26
98	words	2024-08-26
99	words	2024-08-26
100	words	2024-08-26
101	words	2024-08-26
102	words	2024-08-26
103	words	2024-08-26
104	words	2024-08-26
105	words	2024-08-26
106	words	2024-08-26
107	words	2024-08-26
108	words	2024-08-26
109	words	2024-08-26
110	words	2024-08-26
111	words	2024-08-26
112	words	2024-08-26
113	words	2024-08-26
114	words	2024-08-26
115	words	2024-08-26
116	words	2024-08-26
117	words	2024-08-26
118	words	2024-08-26
119	words	2024-08-26
120	words	2024-08-26
121	words	2024-08-26
122	words	2024-08-26
123	words	2024-08-26
124	words	2024-08-26
125	words	2024-08-26
126	words	2024-08-26
127	words	2024-08-26
128	words	2024-08-26
129	words	2024-08-26
130	words	2024-08-26
131	words	2024-08-26
132	words	2024-08-26
133	words	2024-08-26
134	words	2024-08-26
135	words	2024-08-26
136	words	2024-08-26
137	words	2024-08-26
138	words	2024-08-26
139	words	2024-08-26
140	words	2024-08-26
141	words	2024-08-26
142	words	2024-08-26
143	words	2024-08-26
144	words	2024-08-26
145	words	2024-08-26
146	words	2024-08-26
147	words	2024-08-26
148	words	2024-08-26
149	words	2024-08-26
150	words	2024-08-26
151	words	2024-08-26
152	words	2024-08-26
153	words	2024-08-26
154	words	2024-08-26
155	words	2024-08-26
156	words	2024-08-26
157	words	2024-08-26
158	words	2024-08-26
159	words	2024-08-26
160	words	2024-08-26
161	words	2024-08-26
162	words	2024-08-26
163	words	2024-08-26
164	words	2024-08-26
165	words	2024-08-26
166	words	2024-08-26
172	words	2024-08-26
187	words	2024-08-26
199	words	2024-08-26
213	words	2024-08-26
227	words	2024-08-26
241	words	2024-08-26
254	words	2024-08-26
268	words	2024-08-26
167	words	2024-08-26
182	words	2024-08-26
197	words	2024-08-26
212	words	2024-08-26
228	words	2024-08-26
243	words	2024-08-26
258	words	2024-08-26
273	words	2024-08-26
168	words	2024-08-26
183	words	2024-08-26
198	words	2024-08-26
214	words	2024-08-26
229	words	2024-08-26
244	words	2024-08-26
259	words	2024-08-26
275	words	2024-08-26
169	words	2024-08-26
184	words	2024-08-26
200	words	2024-08-26
215	words	2024-08-26
230	words	2024-08-26
245	words	2024-08-26
260	words	2024-08-26
274	words	2024-08-26
170	words	2024-08-26
185	words	2024-08-26
201	words	2024-08-26
205	words	2024-08-26
220	words	2024-08-26
236	words	2024-08-26
251	words	2024-08-26
266	words	2024-08-26
171	words	2024-08-26
186	words	2024-08-26
190	words	2024-08-26
204	words	2024-08-26
219	words	2024-08-26
234	words	2024-08-26
249	words	2024-08-26
264	words	2024-08-26
173	words	2024-08-26
188	words	2024-08-26
203	words	2024-08-26
218	words	2024-08-26
232	words	2024-08-26
246	words	2024-08-26
261	words	2024-08-26
276	words	2024-08-26
174	words	2024-08-26
202	words	2024-08-26
206	words	2024-08-26
222	words	2024-08-26
238	words	2024-08-26
253	words	2024-08-26
269	words	2024-08-26
175	words	2024-08-26
189	words	2024-08-26
217	words	2024-08-26
231	words	2024-08-26
247	words	2024-08-26
263	words	2024-08-26
176	words	2024-08-26
191	words	2024-08-26
225	words	2024-08-26
240	words	2024-08-26
256	words	2024-08-26
270	words	2024-08-26
177	words	2024-08-26
194	words	2024-08-26
209	words	2024-08-26
224	words	2024-08-26
239	words	2024-08-26
255	words	2024-08-26
271	words	2024-08-26
178	words	2024-08-26
192	words	2024-08-26
208	words	2024-08-26
223	words	2024-08-26
237	words	2024-08-26
252	words	2024-08-26
267	words	2024-08-26
179	words	2024-08-26
193	words	2024-08-26
207	words	2024-08-26
221	words	2024-08-26
235	words	2024-08-26
250	words	2024-08-26
265	words	2024-08-26
180	words	2024-08-26
195	words	2024-08-26
211	words	2024-08-26
226	words	2024-08-26
242	words	2024-08-26
257	words	2024-08-26
272	words	2024-08-26
181	words	2024-08-26
196	words	2024-08-26
210	words	2024-08-26
216	words	2024-08-26
233	words	2024-08-26
248	words	2024-08-26
262	words	2024-08-26
277	words	2024-08-26
278	words	2024-08-26
279	words	2024-08-26
280	words	2024-08-26
281	words	2024-08-26
282	words	2024-08-26
283	words	2024-08-26
284	words	2024-08-26
285	words	2024-08-26
286	words	2024-08-26
287	words	2024-08-26
288	words	2024-08-26
289	words	2024-08-26
290	words	2024-08-26
291	words	2024-08-26
292	words	2024-08-26
293	words	2024-08-26
294	words	2024-08-26
295	words	2024-08-26
296	words	2024-08-26
297	words	2024-08-26
298	words	2024-08-26
299	words	2024-08-26
300	words	2024-08-26
301	words	2024-08-26
302	words	2024-08-26
303	words	2024-08-26
304	words	2024-08-26
305	words	2024-08-26
306	words	2024-08-26
307	words	2024-08-26
308	words	2024-08-26
309	words	2024-08-26
310	words	2024-08-26
311	words	2024-08-26
312	words	2024-08-26
313	words	2024-08-26
314	words	2024-08-26
315	words	2024-08-26
316	words	2024-08-26
317	words	2024-08-26
318	words	2024-08-26
319	words	2024-08-26
320	words	2024-08-26
321	words	2024-08-26
322	words	2024-08-26
323	words	2024-08-26
324	words	2024-08-26
325	words	2024-08-26
326	words	2024-08-26
327	words	2024-08-26
328	words	2024-08-26
329	words	2024-08-26
330	words	2024-08-26
331	words	2024-08-26
332	words	2024-08-26
333	words	2024-08-26
334	words	2024-08-26
335	words	2024-08-26
336	words	2024-08-26
337	words	2024-08-26
338	words	2024-08-26
339	words	2024-08-26
340	words	2024-08-26
341	words	2024-08-26
342	words	2024-08-26
343	words	2024-08-26
344	words	2024-08-26
345	words	2024-08-26
346	words	2024-08-26
347	words	2024-08-26
348	words	2024-08-26
349	words	2024-08-26
350	words	2024-08-26
351	words	2024-08-26
352	words	2024-08-26
353	words	2024-08-26
354	words	2024-08-26
355	words	2024-08-26
356	words	2024-08-26
357	words	2024-08-26
358	words	2024-08-26
359	words	2024-08-26
360	words	2024-08-26
361	words	2024-08-26
362	words	2024-08-26
363	words	2024-08-26
364	words	2024-08-26
365	words	2024-08-26
366	words	2024-08-26
367	words	2024-08-26
368	words	2024-08-26
369	words	2024-08-26
370	words	2024-08-26
371	words	2024-08-26
372	words	2024-08-26
373	words	2024-08-26
374	words	2024-08-26
375	words	2024-08-26
376	words	2024-08-26
377	words	2024-08-26
378	words	2024-08-26
379	words	2024-08-26
380	words	2024-08-26
381	words	2024-08-26
382	words	2024-08-26
383	words	2024-08-26
384	words	2024-08-26
385	words	2024-08-26
386	words	2024-08-26
387	words	2024-08-26
388	words	2024-08-26
389	words	2024-08-26
390	words	2024-08-26
391	words	2024-08-26
392	words	2024-08-26
393	words	2024-08-26
394	words	2024-08-26
395	words	2024-08-26
396	words	2024-08-26
397	words	2024-08-26
398	words	2024-08-26
399	words	2024-08-26
400	eat a whole bagel	2024-08-26
401	Read a got dang book	2024-08-26
402	Read a got dang book	2024-08-26
403	words	2024-08-26
404	words	2024-08-26
405	words	2024-08-26
406	words	2024-08-26
407	words	2024-08-26
408	words	2024-08-26
409	words	2024-08-26
410	words	2024-08-26
411	words	2024-08-26
412	words	2024-08-26
413	words	2024-08-26
414	Read a got dang book	2024-08-26
415	eat a whole bagel	2024-08-26
416	eat a whole bagel	2024-08-26
417	eat a whole bagel	2024-08-26
418	words	2024-08-26
419	a whole new assignment	2024-08-26
420	soup baby!	2024-08-26
421	words	2024-08-26
422	eat a whole bagel	2024-08-26
423	eat a whole bagel	2024-08-26
424	soup baby!	2024-08-26
425	Read a got dang book	2024-08-26
426	Read Chapter 5	2024-09-02
427	Read Chapter 5	2024-09-02
428	Read Chapter 5	2024-09-02
429	Read Chapter 5	2024-09-02
430	Read Chapter 5	2024-09-02
431	Read Chapter 5	2024-09-03
432		2024-09-04
433	read words	2024-10-04
\.


--
-- Data for Name: demo_bugs; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.demo_bugs (description, added_by, bug_id) FROM stdin;
delete me please!	anonymous	189
i want to be where the people are	anonymous	212
I want a "complete book" button	anonymous	213
i want to be where the people are	anonymous	224
\.


--
-- Data for Name: demo_syllabus; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.demo_syllabus (book, author, series, is_completed, added_by, season, num_in_series, is_extra_credit, date_completed, up_votes, date_added, genre, down_votes, unique_id) FROM stdin;
Gideon the Ninth	Tamysyn Muir	The Locked Tomb	t		\N	1	f	\N	0	2024-04-04	\N	0	3
Harrow the Ninth	Tamysyn Muir	The Locked Tomb	t		\N	2	f	\N	0	2024-04-04	\N	0	4
Nona the Ninth	Tamysyn Muir	The Locked Tomb	t		\N	3	f	\N	0	2024-04-04	\N	0	5
Alecto the Ninth	Tamysyn Muir	The Locked Tomb	f		\N	4	f	\N	0	2024-04-04	\N	0	6
The Wise Man's Fear	Patrick Rothfuss	The Kingkiller Chronicle	t		\N	2	f	\N	0	2024-04-04	\N	0	8
The Doors of Stone	Patrick Rothfuss	The Kingkiller Chronicle	f		\N	3	f	\N	0	2024-04-04	\N	0	9
The Fifth Season	N. K. Jemisin	Broken Earth trilogy	t		\N	1	f	\N	0	2024-04-04	\N	0	10
The Obelisk Gate	N. K. Jemisin	Broken Earth trilogy	t		\N	2	f	\N	0	2024-04-04	\N	0	11
The Hundred Thousand Kingdoms	N. K. Jemisin	The Inheritance Trilogy	f	mellymi	\N	1	f	\N	0	2023-05-10	\N	0	13
The Broken Kingdoms	N. K. Jemisin	The Inheritance Trilogy	f		\N	2	f	\N	0	2024-04-04	\N	0	14
The Kingdom of Gods	N. K. Jemisin	The Inheritance Trilogy	f		\N	3	f	\N	0	2024-04-04	\N	0	15
Parable of the Sower	Octavia Butler	Parable duology	t		\N	1	f	\N	0	2024-04-04	\N	0	16
Parable of the Talents	Octavia Butler	Parable duology	t	mudgoat	\N	2	t	\N	0	2023-04-10	\N	0	17
The Priory of the Orange Tree	Samantha Shannon	The Priory of the Orange Tree	t	mellymi	\N	1	f	\N	0	2023-05-10	\N	0	19
A Day of Fallen Night	Samantha Shannon	The Priory of the Orange Tree	f	mellymi	\N	1	t	\N	0	2023-05-10	\N	0	20
Iron Widow	Xiran Jay Zhao		f	mudgoat	\N	1	f	\N	0	2024-04-04	\N	0	21
The Poppy War	R. F. Kuang	The Poppy War trilogy	f	mudgoat	\N	1	f	\N	0	2023-02-05	\N	0	24
The Dragon Republic	R. F. Kuang	The Poppy War trilogy	f		\N	2	f	\N	0	2024-04-04	\N	0	25
The Burning God	R. F. Kuang	The Poppy War trilogy	f		\N	3	f	\N	0	2024-04-04	\N	0	26
The Adventures of Amina Al-Sirafi	Shannon Chakraborty	The Adventures of Amina al-Sirafi	f	mudgoat	\N	\N	f	\N	0	2023-04-24	\N	0	29
One Dark Window	Rachel Gillig	The Shepherd King	f	mudgoat	\N	\N	f	\N	0	2023-04-24	\N	0	30
Emily Wilde's Encyclopedia of Faeries	Heather Fawcett	Emily Wilde	f	mudgoat	\N	\N	f	\N	0	2023-04-24	\N	0	31
A Song of Silver and Gold	Melissa Karibian		f	shinibon	\N	\N	f	\N	0	2023-06-05	\N	0	32
Piranesi	Susanna Clarke		f	mudgoat	\N	\N	f	\N	0	2023-09-25	\N	0	35
A Deadly Education	Naomi Novik		f	mudgoat	\N	\N	f	\N	0	2024-03-30	\N	0	39
A Broken Blade	Melissa Blair	The Halfling Sage	f	mudgoat	\N	1	f	\N	0	2024-03-30	\N	0	40
A Shadow Crown	Melissa Blair	The Halfling Sage	f	mudgoat	\N	2	f	\N	0	2024-03-30	\N	0	41
A Vicious Game	Melissa Blair	The Halfling Sage	f	mudgoat	\N	3	f	\N	0	2024-03-30	\N	0	42
Neuromancer	William Gobson		f	mudgoat	\N	\N	f	\N	0	2024-03-30	\N	0	43
Dark Matter	Blake Crouch		f	mudgoat	\N	\N	f	\N	0	2024-03-30	\N	0	44
Klara and the Sun	Kazuo Ishiguro		f	mudgoat	\N	\N	f	\N	0	2024-03-30	\N	0	45
Robot Dreams	Isaac Asimov		f	mudgoat	\N	\N	f	\N	0	2024-03-30	\N	0	46
The Day of the Triffids	John Wyndham		f	mudgoat	\N	\N	f	\N	0	2024-03-30	\N	0	47
The Last House on the Street	Catriona Ward		f	shinibon	\N	\N	f	\N	0	2024-04-01	\N	0	48
Annihilation	Jeff VanderMeer	Southern Reach Trilogy	f	mudgoat	\N	1	f	\N	0	2024-04-04	\N	0	49
Authority	Jeff VanderMeer	Southern Reach Trilogy	f	mudgoat	\N	2	f	\N	0	2024-04-04	\N	0	50
Acceptance	Jeff VanderMeer	Southern Reach Trilogy	f	mudgoat	\N	3	f	\N	0	2024-04-04	\N	0	51
Fourth Wing	Rebecca Yarros	Empyrean	t	mudgoat	\N	\N	f	2024-05-28	0	2023-11-09	\N	0	53
In the Lives of Puppets	TJ Klune		t	mellymi	\N	\N	f	2024-07-27	0	2023-06-10	\N	0	33
Ninefox Gambit	Yoon Ha Lee	Machineries of Empire	t	mudgoat	\N	\N	f	2024-07-27	0	2024-03-29	\N	0	36
A Memory Called Test	Arkady Martine	Teixcalaan	t	mudgoat	2	1	f	2024-09-17	0	2024-03-29		0	37
The Road	Cormac McCarthy		t		0	1	t	2023-06-12	0	2024-04-04		0	18
A Prayer for the Crown-Shy	Becky Chambers	Monk & Robot	t		\N	2	f	2026-03-26	0	2024-04-04	\N	0	23
The Name of the Wind	Patrick Rothfuss	The Kingkiller Chronicle	t		\N	1	f	2024-08-06	0	2024-04-04	\N	0	7
A Psalm for the Wild-Built	Becky Chambers	Monk & Robot	t	mudgoat	\N	1	f	2024-08-08	0	2024-04-04	\N	0	22
444	None		f		0	0	f	\N	0	2024-08-11		0	85
999	author		t		0	0	f	2024-08-11	0	2024-08-11		0	84
book3	author	something evil	t		0	0	f	2024-08-11	0	2024-08-11		0	79
123444	Arkady Martine		t		0	0	f	2024-08-20	0	2024-08-11		0	87
The Rage of Dragons	Evan Winter	The Burning	t		\N	1	f	2024-08-20	0	2022-12-12	\N	0	52
Black Leopard Red Wolf	Marlon James	The Dark Star Trilogy	f	shinibon	0	0	f	2024-08-19	0	2023-04-20		0	28
The Fires of Vengeance	Evan Winter	The Burning	t		\N	2	f	2024-08-20	0	2022-12-12	\N	0	1
The Lord of Demons	Evan Winter	The Burning	t		\N	3	f	2024-08-20	0	2024-04-04	\N	0	2
Jade City	Fonda Lee	Green Bone Saga	t	knamustarsunder	\N	\N	f	2024-08-20	0	2023-03-06	\N	0	27
AAA	BBB	CCC	f	lady testworth	0	\N	f	\N	0	2024-08-21		0	133
AAB	BBB	CCC	f	lady testworth	0	\N	f	\N	0	2024-08-21		0	134
AAC	BBB		f	lady testworth	0	\N	f	\N	0	2024-08-21		0	135
AAD	CBC		f	lady testworth	0	\N	f	\N	0	2024-08-21		0	136
book	author		f	someone	0	0	f	\N	0	2024-08-24		0	137
zzz	zzz, xxx		f	added_by	0	0	f	\N	0	2024-08-24		0	138
This Is How You Lose the Time War	Max Gladstone, Amal El-Mohtar		f	Juni	0	0	f	\N	0	2024-08-24		0	139
The Stone Sky	N. K. Jemisin	Broken Earth trilogy	t		\N	3	f	2024-08-25	0	2024-04-04	\N	0	12
fluke 2	Arkady Martine	the awayness	t		0	0	f	2024-09-18	0	2024-08-26		0	140
fluke 2	Arkady Martine	the awayness	f		0	0	f	\N	0	2024-08-26		0	145
fluke 2	Arkady Martine	the awayness	f		0	0	f	\N	0	2024-08-26		0	153
aaaaa	aaaaa	aaaaaa	f		0	0	f	\N	0	2024-08-26		0	154
\.


--
-- Data for Name: syllabus; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.syllabus (book, author, series, is_completed, added_by, season, num_in_series, is_extra_credit, date_completed, up_votes, date_added, genre, unique_id, down_votes) FROM stdin;
The Lord of Demons	Evan Winter	The Burning	f		\N	3	f	\N	0	2024-04-04	\N	3	0
Alecto the Ninth	Tamysyn Muir	The Locked Tomb	f		\N	4	f	\N	0	2024-04-04	\N	7	0
The Doors of Stone	Patrick Rothfuss	The Kingkiller Chronicle	f		\N	3	f	\N	0	2024-04-04	\N	10	0
The Hundred Thousand Kingdoms	N. K. Jemisin	The Inheritance Trilogy	f	mellymi	\N	1	f	\N	0	2023-05-10	\N	14	0
The Broken Kingdoms	N. K. Jemisin	The Inheritance Trilogy	f		\N	2	f	\N	0	2024-04-04	\N	15	0
The Kingdom of Gods	N. K. Jemisin	The Inheritance Trilogy	f		\N	3	f	\N	0	2024-04-04	\N	16	0
A Day of Fallen Night	Samantha Shannon	The Priory of the Orange Tree	f	mellymi	\N	1	t	\N	0	2023-05-10	\N	21	0
The Dragon Republic	R. F. Kuang	The Poppy War trilogy	f		\N	2	f	\N	0	2024-04-04	\N	26	0
The Burning God	R. F. Kuang	The Poppy War trilogy	f		\N	3	f	\N	0	2024-04-04	\N	27	0
Jade City	Fonda Lee	Green Bone Saga	f	knamustarsunder	\N	\N	f	\N	0	2023-03-06	\N	28	0
The Adventures of Amina Al-Sirafi	Shannon Chakraborty	The Adventures of Amina al-Sirafi	f	mudgoat	\N	\N	f	\N	0	2023-04-24	\N	30	0
One Dark Window	Rachel Gillig	The Shepherd King	f	mudgoat	\N	\N	f	\N	0	2023-04-24	\N	31	0
In the Lives of Puppets	TJ Klune		f	mellymi	\N	\N	f	\N	0	2023-06-10	\N	34	0
Piranesi	Susanna Clarke		f	mudgoat	\N	\N	f	\N	0	2023-09-25	\N	36	0
Ninefox Gambit	Yoon Ha Lee	Machineries of Empire	f	mudgoat	\N	\N	f	\N	0	2024-03-29	\N	38	0
A Memory Called Empire	Arkady Martine	Teixcalaan 	f	mudgoat	\N	1	f	\N	0	2024-03-29	\N	39	0
A Desolation Called Peace	Arkady Martine	Teixcalaan 	f	mudgoat	\N	2	f	\N	0	2024-03-29	\N	40	0
A Deadly Education	Naomi Novik		f	mudgoat	\N	\N	f	\N	0	2024-03-30	\N	41	0
A Broken Blade	Melissa Blair	The Halfling Sage	f	mudgoat	\N	1	f	\N	0	2024-03-30	\N	42	0
A Shadow Crown	Melissa Blair	The Halfling Sage	f	mudgoat	\N	2	f	\N	0	2024-03-30	\N	43	0
A Vicious Game	Melissa Blair	The Halfling Sage	f	mudgoat	\N	3	f	\N	0	2024-03-30	\N	44	0
Neuromancer	William Gobson		f	mudgoat	\N	\N	f	\N	0	2024-03-30	\N	45	0
Dark Matter	Blake Crouch		f	mudgoat	\N	\N	f	\N	0	2024-03-30	\N	46	0
Klara and the Sun	Kazuo Ishiguro		f	mudgoat	\N	\N	f	\N	0	2024-03-30	\N	47	0
Robot Dreams	Isaac Asimov		f	mudgoat	\N	\N	f	\N	0	2024-03-30	\N	48	0
The Day of the Triffids	John Wyndham		f	mudgoat	\N	\N	f	\N	0	2024-03-30	\N	49	0
How to Become the Dark Lord and Die Trying	Django Wexler		f	Juni	0	0	f	\N	0	2024-08-24	Time looping MC	71	0
The Last House on Needless Street	Catriona Ward		f	shinibon	0	0	f	\N	0	2024-04-01		50	0
A Song of Silver and Gold	Melissa Karibian		f	shinibon	0	0	f	\N	0	2023-06-05	sapphic mermaids	33	0
This Is How You Lose the Time War	Max Gladstone, Amal El-Mohtar		f		0	0	f	\N	0	2024-08-24		72	0
Acceptance	Jeff VanderMeer	Southern Reach Trilogy	t	mudgoat	\N	3	f	2025-01-21	0	2024-04-04	\N	53	0
The Wise Man's Fear	Patrick Rothfuss	The Kingkiller Chronicle	t		3	2	f	2025-04-01	0	2024-04-04		9	0
The Fires of Vengeance	Evan Winter	The Burning	t		4	2	f	2025-11-18	0	2022-12-12		2	0
The Stone Sky	N. K. Jemisin	Broken Earth trilogy	t		2	3	f	2025-04-01	0	2024-04-04		13	0
A Psalm for the Wild-Built	Becky Chambers	Monk & Robot	t	mudgoat	\N	1	f	2025-09-23	0	2024-04-04	\N	23	0
Gideon the Ninth	Tamysyn Muir	The Locked Tomb	t		3	1	f	\N	1	2024-04-04		4	0
Harrow the Ninth	Tamysyn Muir	The Locked Tomb	t		4	2	f	\N	1	2024-04-04		5	0
Nona the Ninth	Tamysyn Muir	The Locked Tomb	t		4	3	f	\N	1	2024-04-04		6	0
Black Leopard Red Wolf	Marlon James	The Dark Star Trilogy	t	shinibon	5	1	f	2024-08-27	0	2023-04-20		29	0
Parable of the Sower	Octavia Butler	Parable duology	t		3	1	f	2025-03-18	0	2024-04-04		17	0
Dungeon Crawler Carl	Matt Dinniman		f	mudgoat	0	\N	f	\N	0	2025-04-01		76	0
A Prayer for the Crown-Shy	Becky Chambers	Monk & Robot	t		0	2	f	2025-04-01	0	2024-04-04		24	0
The Name of the Wind	Patrick Rothfuss	The Kingkiller Chronicle	t		1	1	f	2025-04-01	0	2024-04-04		8	0
Annihilation	Jeff VanderMeer	Southern Reach Trilogy	t	mudgoat	6	1	f	2024-09-24	0	2024-04-04		51	0
Authority	Jeff VanderMeer	Southern Reach Trilogy	t	mudgoat	\N	2	f	2025-01-21	0	2024-04-04	\N	52	0
Parable of the Talents	Octavia Butler	Parable duology	t	mudgoat	\N	2	t	2025-03-18	0	2023-04-10	\N	18	0
Iron Flame	Rebecca Yarros	Empyrean	t	mudgoat	0	2	f	2025-01-21	0	2025-01-21		73	0
Fourth Wing	Rebecca Yarros	Empyrean	t	mudgoat	5	1	f	2024-05-28	0	2023-11-09		37	1
Sons of Darkness	Gourav Mohanty	The Raag of Rta	f	Phil	0	1	f	\N	0	2025-01-28	Game of Thrones but India	74	0
The Priory of the Orange Tree	Samantha Shannon	The Priory of the Orange Tree	t	mellymi	5	1	f	2025-03-18	0	2023-05-10		20	0
The Poppy War	R. F. Kuang	The Poppy War trilogy	t	mudgoat	\N	1	f	2025-04-01	0	2023-02-05	\N	25	0
The Sapling Cage	Maragaret Killjoy		f	mudgoat	0	\N	f	\N	0	2025-04-01		77	0
The Fifth Season	N. K. Jemisin	Broken Earth trilogy	t		2	1	f	2025-04-01	0	2024-04-04		11	0
The Obelisk Gate	N. K. Jemisin	Broken Earth trilogy	t		2	2	f	2025-04-01	0	2024-04-04		12	0
Onyx Storm	Rebecca Yarros	Empyrean	f	kiburi	0	\N	f	\N	0	2025-04-01		79	0
The Never Tilting World	Rin Chupeco		f	therivertam	0	\N	f	\N	0	2025-04-01		80	0
The Road	Cormac McCarthy		t		2	1	t	2025-04-01	0	2024-04-04		19	0
The Rage of Dragons	Evan Winter	The Burning	t		1	1	f	2025-11-18	0	2022-12-12		1	0
Emily Wilde's Encyclopedia of Faeries	Heather Fawcett	Emily Wilde	t	mudgoat	\N	\N	f	2025-11-18	0	2023-04-24	\N	32	0
Moon Witch Spider King	Marlon James	The Dark Star Trilogy	t		0	2	f	2025-11-18	0	2025-03-18		75	0
Iron Widow	Xiran Jay Zhao		t	mudgoat	0	1	f	2025-11-18	1	2024-04-04		22	0
The Long Way to a Small,  Angry Planet	Becky Chambers	Wayfarers	f	brigadier7527	0	1	f	2025-11-18	1	2023-06-30		35	0
Even Though I Knew The End	C.L. Polk		t	therivertam	0	\N	f	2025-11-18	0	2025-04-01		78	0
Emily Wilde's Map of the Otherlands	Heather Fawcett	Emily Wilde Series	t		0	2	f	2026-01-20	0	2026-01-20	fantasy 	81	0
Upon a Burning Throne	Ashok K. Banker	The Burnt Empire Saga	f	Phil	0	1	f	\N	0	2026-02-24	fantasy, India, 	82	0
Black Sun	Rebecca RoanHorse	Between Earth and Sky	f	Phil	0	0	f	\N	0	2026-02-24	Indigenous, Fantasy Fiction LGBT Science Fiction Queer	84	0
To Shape a Dragon's Breath	Moniquill Blackgoose	Nampeshiweisit	f	Phil	0	1	f	\N	0	2026-02-24	Fantasy Dragons Young Adult Fiction Queer LGBT Indigenous	85	0
\.


--
-- Name: assignments_assignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.assignments_assignment_id_seq', 85, true);


--
-- Name: bugs_bug_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.bugs_bug_id_seq', 60, true);


--
-- Name: demo_assignments_assignment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.demo_assignments_assignment_id_seq', 433, true);


--
-- Name: demo_bugs_bug_id_temp_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.demo_bugs_bug_id_temp_seq', 230, true);


--
-- Name: demo_syllabus_unique_id_temp_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.demo_syllabus_unique_id_temp_seq', 433, true);


--
-- Name: syllabus_newuniqueid_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.syllabus_newuniqueid_seq', 85, true);


--
-- Name: app_config app_config_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.app_config
    ADD CONSTRAINT app_config_pkey PRIMARY KEY (key);


--
-- Name: assignments assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.assignments
    ADD CONSTRAINT assignments_pkey PRIMARY KEY (assignment_id);


--
-- Name: bugs bugs_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.bugs
    ADD CONSTRAINT bugs_pkey PRIMARY KEY (bug_id);


--
-- Name: demo_assignments demo_assignments_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.demo_assignments
    ADD CONSTRAINT demo_assignments_pkey PRIMARY KEY (assignment_id);


--
-- Name: demo_bugs demo_bugs_bug_id_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.demo_bugs
    ADD CONSTRAINT demo_bugs_bug_id_key UNIQUE (bug_id);


--
-- Name: demo_syllabus demo_syllabus_unique_id_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.demo_syllabus
    ADD CONSTRAINT demo_syllabus_unique_id_key UNIQUE (unique_id);


--
-- Name: ix_assignments_assignment_id; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX ix_assignments_assignment_id ON public.assignments USING btree (assignment_id);


--
-- Name: ix_assignments_description; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX ix_assignments_description ON public.assignments USING btree (description);


--
-- Name: ix_demo_assignments_assignment_id; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX ix_demo_assignments_assignment_id ON public.demo_assignments USING btree (assignment_id);


--
-- Name: ix_demo_assignments_description; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX ix_demo_assignments_description ON public.demo_assignments USING btree (description);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON TABLES TO neon_superuser WITH GRANT OPTION;


--
-- PostgreSQL database dump complete
--

\unrestrict 9vjkKWaBUykxlYshpaHFZpW1omnczpC59fMOpeFOBEPw9baTlAFzUQTaOk6xPFj

