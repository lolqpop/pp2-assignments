ALTER TABLE public.phonebook 
ADD CONSTRAINT unique_first_name UNIQUE (first_name);



CREATE OR REPLACE FUNCTION find_contacts(search_pattern TEXT)
RETURNS TABLE (user_id INT, first_name VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.user_id, p.first_name, p.phone_number 
    FROM public.phonebook p
    WHERE p.first_name ILIKE '%' || search_pattern || '%'
       OR p.phone_number LIKE '%' || search_pattern || '%';
END;
$$ LANGUAGE plpgsql;




CREATE OR REPLACE FUNCTION get_phonebook_paged(p_limit INT, p_offset INT)
RETURNS SETOF public.phonebook AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM public.phonebook
    ORDER BY user_id ASC
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;