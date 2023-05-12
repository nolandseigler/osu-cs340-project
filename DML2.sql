-- Queries use a colon : character to 
-- denote the variables that will have data from the backend programming language

INSERT INTO `cs340_seiglern`.`office_types` (code, name)
VALUES
	(:code_input, :name_input);
    

INSERT INTO `cs340_seiglern`.`contributor_types` (code, name)
VALUES
    (:code_input, :name_input);

INSERT INTO `cs340_seiglern`.`report_types` (code, name)
VALUES
    (:code_input, :name_input);
    
INSERT INTO `cs340_seiglern`.`party_types` (code, short_name)
VALUES
    (:code_input, :short_name_input);
    

INSERT INTO `cs340_seiglern`.`incumbent_challenger_statuses` (code, name)
VALUES
    (:code_input, :name_input);

INSERT INTO `cs340_seiglern`.`amendment_indicators` (code, name)
VALUES
    (:code_input, :name_input);


INSERT INTO `cs340_seiglern`.`election_years` (year)
VALUES
    (:year_input)



INSERT INTO `cs340_seiglern`.`transaction_types` (code, name)
VALUES
    (:code_input, :name_input);

INSERT INTO `cs340_seiglern`.`candidates` (first_name, last_name, middle_name, email)
VALUES 
    (:first_name_input, :last_name_input, :middle_name_input, :email_input)


INSERT INTO `cs340_seiglern`.`candidate_office_records` (
    fec_cand_id,
    name,
    ttl_receipts,
    trans_from_auth,
    coh_bop,
    coh_cop,
    cand_contrib,
    cand_loans,
    other_loans,
    cand_loan_repay,
    other_loan_repay,
    debts_owed_by,
    ttl_indiv_contrib,
    cand_office_st,
    cand_office_district,
    pol_pty_contrib,
    cvg_end_dt,
    indiv_refund,
    cmte_refund,
    office_types_id,
    candidates_id,
    party_types_id,
    incumbent_challenger_statuses_id
) VALUES (
    fec_cand_id,
    name,
    ttl_receipts,
    trans_from_auth,
    coh_bop,
    coh_cop,
    cand_contrib,
    cand_loans,
    other_loans,
    cand_loan_repay,
    other_loan_repay,
    debts_owed_by,
    ttl_indiv_contrib,
    cand_office_st,
    cand_office_district,
    pol_pty_contrib,
    cvg_end_dt,
    indiv_refund,
    cmte_refund,
    (SELECT id FROM `cs340_seiglern`.`office_types` WHERE code = :office_types_code_input),
    NULL,
    (SELECT id FROM `cs340_seiglern`.`party_types` WHERE short_name = :short_name_input),
    (SELECT id FROM `cs340_seiglern`.`incumbent_challenger_statuses` WHERE code = :incumbent_challenger_statuses_code_input)
);


INSERT INTO `cs340_seiglern`.`committee_types` (code, name, explanation)
VALUES
    (:code_input, :name_input, :explanation_input)



INSERT INTO `cs340_seiglern`.`committees` (
    cmte_id,
    name,
    city,
    state,
    zip_code,
    committee_types_id
) VALUES
(
    :cmte_id_input,
    :name_input,
    :city_input,
    :state_input,
    :zip_code_input,
    (SELECT id FROM `cs340_seiglern`.`committee_types` WHERE code = :committee_types_code_input)
);


INSERT INTO `cs340_seiglern`.`contributions` (
    transaction_pgi,
    image_num,
    transaction_dt,
    transaction_amt,
    trans_id,
    file_num,
    memo_cd,
    memo_text,
    sub_id,
    committees_id,
    report_types_id,
    transaction_types_id,
    amendment_indicators_id,
    contributor_types_id
) VALUES 
(
    :transaction_pgi_input,
    :image_num_input,
    :transaction_dt_input,
    :transaction_amt_input,
    :trans_id_input,
    :file_num_input,
    :memo_cd_input,
    :memo_text_input,
    :sub_id_input,
    (SELECT id FROM `cs340_seiglern`.`committees` WHERE cmte_id = :committees_cmte_id_input_from_dropdown),
    (SELECT id FROM `cs340_seiglern`.`report_types` WHERE code = :report_types_code_input_from_dropdown),
    (SELECT id FROM `cs340_seiglern`.`transaction_types` WHERE code = :transaction_types_code_input_from_dropdown),
    (SELECT id FROM `cs340_seiglern`.`amendment_indicators` WHERE code = :amendment_indicators_code_input_from_dropdown),
    (SELECT id FROM `cs340_seiglern`.`contributor_types` WHERE code = :contributor_types_code_input_from_dropdown);
)




-- EVEN YEARS ONLY FOR CYCLES
INSERT INTO `cs340_seiglern`.`cycles` (year)
VALUES
    (:year_input);


INSERT INTO `cs340_seiglern`.`candidate_office_records_committees`(
    candidate_office_records_id,
    committees_id
) VALUES
    (
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = :candidate_office_records_fec_cand_id_input_from_dropdown
        ),
        (
            SELECT id FROM `cs340_seiglern`.`committees` 
            WHERE cmte_id = :committees_cmte_id_input_from_dropdown
        )
    );

INSERT INTO `cs340_seiglern`.`candidate_office_records_contributions`(
    candidate_office_records_id,
    contributions_id
) VALUES
    (
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = :candidate_office_records_fec_cand_id_input_from_dropdown
        ),
        (
            SELECT id FROM `cs340_seiglern`.`contributions` 
            WHERE sub_id = :contributions_sub_id_input_from_dropdown
        )
    );


INSERT INTO `cs340_seiglern`.`election_years_contributions`(
    election_years_year,
    contributions_id
) VALUES
    (
        (
            SELECT year FROM `cs340_seiglern`.`election_years` 
            WHERE year = :election_years_year_input_from_drop_down
        ),
        (
            SELECT id FROM `cs340_seiglern`.`contributions` 
            WHERE sub_id = :contributions_sub_id_input_from_dropdown
        )
    );


INSERT INTO `cs340_seiglern`.`cycles_contributions`(
    cycles_year,
    contributions_id
) VALUES
    (
        (
            SELECT year FROM `cs340_seiglern`.`cycles` 
            WHERE year = '2024'
        ),
        (
            SELECT id FROM `cs340_seiglern`.`contributions` 
            WHERE sub_id = 4022120231732517006 -- we use sub_id because we know this is a unique fec id for the row in the original data
        )
    ),
    (
        (
            SELECT year FROM `cs340_seiglern`.`cycles` 
            WHERE year = '2024'
        ),
        (
            SELECT id FROM `cs340_seiglern`.`contributions` 
            WHERE sub_id = 4081320211326551161 -- we use sub_id because we know this is a unique fec id for the row in the original data
        )
    ),
    (
        (
            SELECT year FROM `cs340_seiglern`.`cycles` 
            WHERE year = '2024'
        ),
        (
            SELECT id FROM `cs340_seiglern`.`contributions` 
            WHERE sub_id = 4073020221553612171 -- we use sub_id because we know this is a unique fec id for the row in the original data
        )
    );

/* 
For candidate election years and cycles it is a bit tricky.
We know how to get election years from the master candidate record.
We know how to get election years from the contributions data (see above comment block for election_years_contributions)
We know how to get cycles years from the contributions data (see above comment block for cycles_contributions)

We also know that a candidate record can exist for an election year without any contributions.
Scope doesnt allow us to go dig up and analyze all the FEC data but we will do the best with what we know.

For each data source we will insert on conflict do nothing the appropriate values.
Just kidding mysql docs and research tell me that is not supported in mysql or mariadb like it is in postgres

# Citation for the following code:
# Date: 05/04/2023
# Copied from /OR/ Adapted from /OR/ Based on:
https://stackoverflow.com/a/4596409

We just always need to be sure not to mix in dupes so one insert per data source.
*/
INSERT INTO `cs340_seiglern`.`election_years_candidate_office_records`(
    election_years_year,
    candidate_office_records_id
) VALUES
    (
        '2024',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'P80001571'
        )
    ),
    (
        '2024',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'P80000722'
        )
    ),
    (
        '2022',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'H2AK00226'
        )
    ),
    (
        '2022',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'H8NY15148'
        )
    )
ON DUPLICATE KEY UPDATE election_years_year=election_years_year, candidate_office_records_id=candidate_office_records_id;

-- do it again for proof that we are seriousssss. (pretend this is another data source)
INSERT INTO `cs340_seiglern`.`election_years_candidate_office_records`(
    election_years_year,
    candidate_office_records_id
) VALUES
    (
        '2024',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'P80001571'
        )
    ),
    (
        '2024',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'P80000722'
        )
    ),
    (
        '2022',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'H2AK00226'
        )
    ),
    (
        '2022',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'H8NY15148'
        )
    )
ON DUPLICATE KEY UPDATE election_years_year=election_years_year, candidate_office_records_id=candidate_office_records_id;

-- DO cycles now same way

INSERT INTO `cs340_seiglern`.`cycles_candidate_office_records`(
    cycles_year,
    candidate_office_records_id
) VALUES
    (
        '2024',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'P80001571'
        )
    ),
    (
        '2024',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'P80000722'
        )
    ),
    (
        '2022',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'H2AK00226'
        )
    ),
    (
        '2022',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'H8NY15148'
        )
    )
ON DUPLICATE KEY UPDATE cycles_year=cycles_year, candidate_office_records_id=candidate_office_records_id;

-- do it again for proof that we are seriousssss. (pretend this is another data source)
INSERT INTO `cs340_seiglern`.`cycles_candidate_office_records`(
    cycles_year,
    candidate_office_records_id
) VALUES
    (
        '2024',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'P80001571'
        )
    ),
    (
        '2024',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'P80000722'
        )
    ),
    (
        '2022',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'H2AK00226'
        )
    ),
    (
        '2022',
        (
            SELECT id FROM `cs340_seiglern`.`candidate_office_records` 
            WHERE fec_cand_id = 'H8NY15148'
        )
    )
ON DUPLICATE KEY UPDATE cycles_year=cycles_year, candidate_office_records_id=candidate_office_records_id;