PGDMP                       }           library_management    17.2    17.2     ,           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            -           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            .           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            /           1262    16388    library_management    DATABASE     �   CREATE DATABASE library_management WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Portuguese_Brazil.1252';
 "   DROP DATABASE library_management;
                     postgres    false            �            1259    24606    books    TABLE     �   CREATE TABLE public.books (
    id integer NOT NULL,
    title character varying(255),
    author character varying(255),
    genre character varying(255)
);
    DROP TABLE public.books;
       public         heap r       postgres    false            �            1259    24605    books_id_seq    SEQUENCE     �   CREATE SEQUENCE public.books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.books_id_seq;
       public               postgres    false    220            0           0    0    books_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.books_id_seq OWNED BY public.books.id;
          public               postgres    false    219            �            1259    24597    login    TABLE     �   CREATE TABLE public.login (
    id integer NOT NULL,
    username character varying(50) NOT NULL,
    password character varying(255) NOT NULL
);
    DROP TABLE public.login;
       public         heap r       postgres    false            �            1259    24596    login_id_seq    SEQUENCE     �   CREATE SEQUENCE public.login_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 #   DROP SEQUENCE public.login_id_seq;
       public               postgres    false    218            1           0    0    login_id_seq    SEQUENCE OWNED BY     =   ALTER SEQUENCE public.login_id_seq OWNED BY public.login.id;
          public               postgres    false    217            �           2604    24609    books id    DEFAULT     d   ALTER TABLE ONLY public.books ALTER COLUMN id SET DEFAULT nextval('public.books_id_seq'::regclass);
 7   ALTER TABLE public.books ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    220    219    220            �           2604    24600    login id    DEFAULT     d   ALTER TABLE ONLY public.login ALTER COLUMN id SET DEFAULT nextval('public.login_id_seq'::regclass);
 7   ALTER TABLE public.login ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    218    217    218            )          0    24606    books 
   TABLE DATA           9   COPY public.books (id, title, author, genre) FROM stdin;
    public               postgres    false    220   f       '          0    24597    login 
   TABLE DATA           7   COPY public.login (id, username, password) FROM stdin;
    public               postgres    false    218   �       2           0    0    books_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.books_id_seq', 1, false);
          public               postgres    false    219            3           0    0    login_id_seq    SEQUENCE SET     :   SELECT pg_catalog.setval('public.login_id_seq', 3, true);
          public               postgres    false    217            �           2606    24613    books books_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.books DROP CONSTRAINT books_pkey;
       public                 postgres    false    220            �           2606    24615    books books_title_key 
   CONSTRAINT     Q   ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_title_key UNIQUE (title);
 ?   ALTER TABLE ONLY public.books DROP CONSTRAINT books_title_key;
       public                 postgres    false    220            �           2606    24602    login login_pkey 
   CONSTRAINT     N   ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_pkey PRIMARY KEY (id);
 :   ALTER TABLE ONLY public.login DROP CONSTRAINT login_pkey;
       public                 postgres    false    218            �           2606    24604    login login_username_key 
   CONSTRAINT     W   ALTER TABLE ONLY public.login
    ADD CONSTRAINT login_username_key UNIQUE (username);
 B   ALTER TABLE ONLY public.login DROP CONSTRAINT login_username_key;
       public                 postgres    false    218            )      x������ � �      '   �   x�5���@  �u���)ђp"�I=���T�$�I}���W�HNk&�0�U(C�=��v'��N�-�B
�O�G��v��!���jE7�Y�/�5�R�R����;�}1�z�w�R\Υ�n���)ʲ�4�:e�F�t����y4�i�1�����hXW9��i\��
����̜e�y�D��.C�2f�� ��A�     