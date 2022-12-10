DO $$
    DECLARE
        id  Place.id%TYPE;

    BEGIN
        id := 0
        FOR counter IN 1..5
            LOOP
                INSERT INTO Place(place_id)
                VALUES (id + counter);
            END LOOP;
    END;
$$