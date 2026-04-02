CREATE OR REPLACE PROCEDURE upsert_contact(p_name TEXT, p_phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    INSERT INTO public.phonebook (first_name, phone_number)
    VALUES (p_name, p_phone)
    ON CONFLICT (first_name) 
    DO UPDATE SET phone_number = EXCLUDED.phone_number;
END;
$$;




CREATE OR REPLACE FUNCTION bulk_insert_contacts(names TEXT[], phones TEXT[])
RETURNS TABLE (rejected_name TEXT, rejected_phone TEXT) AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(names, 1) LOOP
        IF length(phones[i]) >= 5 THEN
            INSERT INTO public.phonebook (first_name, phone_number) 
            VALUES (names[i], phones[i])
            ON CONFLICT (first_name) DO NOTHING;
        ELSE
            rejected_name := names[i];
            rejected_phone := phones[i];
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;