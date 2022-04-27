SELECT*
FROM  sr, cs
WHERE sr.client_snap_id = cs.id
        AND sr.b_enable = '1'