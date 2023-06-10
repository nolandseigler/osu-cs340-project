
/*
Group Name: Team FEC (Group 35)
Group Members: Noland Seigler & Jennifer Um
Project Title: Federal Election Committee’s Candidate Funding Sources Database
Assignment: Project Step 3 Draft

*/


/*
READ Entities

amendment_indicators
candidates
candidate_office_records
committee_types
committees
contributions
contributor_types
cycles
election_years
incumbent_challenger_statuses
office_types
party_types
report_types
transaction_types

*/

SELECT * FROM `candidates`;

SELECT `candidate_office_records`.id,
 fec_cand_id,
 `candidate_office_records`.name,
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
 `office_types`.name as office_type,
 `candidates`.email as candidate_email,
 `party_types`.short_name as party_type,
 `incumbent_challenger_statuses`.name as incumbent_challenger_status
FROM `candidate_office_records`
 INNER JOIN `office_types` on `candidate_office_records`.office_types_id = `office_types`.id
 LEFT OUTER JOIN `candidates` on `candidate_office_records`.candidates_id = `candidates`.id
 INNER JOIN `party_types` on `candidate_office_records`.party_types_id = `party_types`.id
 INNER JOIN `incumbent_challenger_statuses` on `candidate_office_records`.incumbent_challenger_statuses_id = `incumbent_challenger_statuses`.id;



SELECT `committees`.id, 'cmte_id', 'name', 'city', 'state', 'zip_code', `committee_types`.name as committee_type
 FROM `committees` 
 INNER JOIN `committee_types` 
 ON `committees`.committee_types_id = `committee_types`.id;


SELECT `contributions`.id,
 transaction_pgi,
 image_num,
 transaction_dt,
 transaction_amt,
 trans_id,
 file_num,
 memo_cd,
 memo_text,
 sub_id,
 `committees`.name as committee,
 `report_types`.name as report_type,
 `transaction_types`.name as transaction_type,
 `amendment_indicators`.name as amendment_indicator,
 `contributor_types`.name as contributor_type
FROM `contributions`
 INNER JOIN `committees` on `contributions`.committees_id = `committees`.id
 INNER JOIN `report_types` on `contributions`.report_types_id = `report_types`.id
 INNER JOIN `transaction_types` on `contributions`.transaction_types_id = `transaction_types`.id
 INNER JOIN `amendment_indicators` on `contributions`.amendment_indicators_id = `amendment_indicators`.id
 INNER JOIN `contributor_types` on `contributions`.contributor_types_id = `contributor_types`.id;

SELECT * FROM cycles;

SELECT * FROM election_years;

SELECT * FROM office_types;
SELECT * FROM contributor_types;
SELECT * FROM committee_types;
SELECT * FROM transaction_types;
SELECT * FROM report_types;
SELECT * FROM party_types;
SELECT * FROM incumbent_challenger_statuses;
SELECT * FROM amendment_indicators;

SELECT * FROM candidate_office_records_committees;
SELECT * FROM candidate_office_records_contributions;
SELECT * FROM election_years_contributions;
SELECT * FROM election_years_candidate_office_records;
SELECT * FROM cycles_contributions;
SELECT * FROM cycles_candidate_office_records;

-- END Read

/*
WRITE Entities

INSERT
amendment_indicators
candidates
candidate_office_records
committee_types
committees
contributions
contributor_types
cycles
election_years
incumbent_challenger_statuses
office_types
party_types
report_types
transaction_types


DELETE
    Entity: 
    M:M: 

UPDATE(Set Null)
    Entity: candidate_office_record.candidate_id

*/
-- Queries use a colon : character to 
-- denote the variables that will have data from the backend programming language

INSERT INTO `office_types` (code, name)
VALUES
	(:code_input, :name_input);
    

INSERT INTO `contributor_types` (code, name)
VALUES
    (:code_input, :name_input);

INSERT INTO `report_types` (code, name)
VALUES
    (:code_input, :name_input);
    
INSERT INTO `party_types` (code, short_name)
VALUES
    (:code_input, :short_name_input);
    
INSERT INTO `incumbent_challenger_statuses` (code, name)
VALUES
    (:code_input, :name_input);

INSERT INTO `amendment_indicators` (code, name)
VALUES
    (:code_input, :name_input);


INSERT INTO `election_years` (year)
VALUES
    (:year_input)


INSERT INTO `transaction_types` (code, name)
VALUES
    (:code_input, :name_input);

INSERT INTO `candidates` (first_name, last_name, middle_name, email)
VALUES 
    (:first_name_input, :last_name_input, :middle_name_input, :email_input)


INSERT INTO `candidate_office_records` (
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
    :fec_cand_id_input,
    :name_input,
    :ttl_receipts_input,
    :trans_from_auth_input,
    :coh_bop_input,
    :coh_cop_input,
    :cand_contrib_input,
    :cand_loans_input,
    :other_loans_input,
    :cand_loan_repay_input,
    :other_loan_repay_input,
    :debts_owed_by_input,
    :ttl_indiv_contrib_input,
    :cand_office_st_input,
    :cand_office_district_input,
    :pol_pty_contrib_input,
    :cvg_end_dt_input,
    :indiv_refund_input,
    :cmte_refund_input,
    (SELECT id FROM `office_types` WHERE code = :office_types_code_input),
    :optional if present -> (SELECT id FROM `candidates` WHERE email = :candidates_email_input_from_drop_down),
    (SELECT id FROM `party_types` WHERE short_name = :short_name_input),
    (SELECT id FROM `incumbent_challenger_statuses` WHERE code = :incumbent_challenger_statuses_code_input)
);


INSERT INTO `committee_types` (code, name, explanation)
VALUES
    (:code_input, :name_input, :explanation_input)



INSERT INTO `committees` (
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
    (SELECT id FROM `committee_types` WHERE name = :committee_types_name_input)
);


INSERT INTO `contributions` (
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
    (SELECT id FROM `committees` WHERE cmte_id = :committees_cmte_id_input_from_dropdown),
    (SELECT id FROM `report_types` WHERE code = :report_types_code_input_from_dropdown),
    (SELECT id FROM `transaction_types` WHERE code = :transaction_types_code_input_from_dropdown),
    (SELECT id FROM `amendment_indicators` WHERE code = :amendment_indicators_code_input_from_dropdown),
    (SELECT id FROM `contributor_types` WHERE code = :contributor_types_code_input_from_dropdown);
)




-- EVEN YEARS ONLY FOR CYCLES
INSERT INTO `cycles` (year)
VALUES
    (:year_input);


INSERT INTO `candidate_office_records_committees`(
    candidate_office_records_id,
    committees_id
) VALUES
    (
        (
            SELECT id FROM `candidate_office_records` 
            WHERE id = :candidate_office_records_id
        ),
        (
            SELECT id FROM `committees` 
            WHERE id = :committees_id
        )
    );

INSERT INTO `candidate_office_records_contributions`(
    candidate_office_records_id,
    contributions_id
) VALUES
    (
        (
            SELECT id FROM `candidate_office_records` 
            WHERE id = :candidate_office_records_id
        ),
        (
            SELECT id FROM `contributions` 
            WHERE id = :contributions_id
        )
    );


INSERT INTO `election_years_contributions`(
    election_years_year,
    contributions_id
) VALUES
    (
        (
            SELECT year FROM `election_years` 
            WHERE year = :election_years_year
        ),
        (
            SELECT id FROM `contributions` 
            WHERE id = :contributions_id
        )
    );


INSERT INTO `cycles_contributions`(
    cycles_year,
    contributions_id
) VALUES
    (
        (
            SELECT year FROM `cycles` 
            WHERE year = :cycles_year
        ),
        (
            SELECT id FROM `contributions` 
            WHERE id = :contributions_id
        )
    );

INSERT INTO `election_years_candidate_office_records`(
    election_years_year,
    candidate_office_records_id
) VALUES
    (
        :election_years_year_input_from_drop_down,
        (
            SELECT id FROM `candidate_office_records`,
            WHERE id = :candidate_office_records_id
        )
    );


INSERT INTO `cycles_candidate_office_records`(
    cycles_year,
    candidate_office_records_id
) VALUES
    (
        :cycles_year,
        (
            SELECT id FROM `candidate_office_records` 
            WHERE id = :candidate_office_records_id
        )
    );


-- UPDATE

UPDATE `candidate_office_records`
SET candidates_id = NULL | (
    SELECT id FROM `candidates` 
    WHERE email = :candidates_email_input_from_dropdown
)
WHERE name = :name_input_from_drop_down;

UPDATE `candidate_office_records_committees`
SET
    candidate_office_records_id = (
        SELECT id FROM `candidate_office_records` 
        WHERE fec_cand_id = :updated_fec_cand_id
    ),
    committees_id = (
        SELECT id FROM `committees` 
        WHERE cmte_id = :updated_cmte_id
    )
WHERE
    candidate_office_records_id = :candidate_office_records_id
    AND committees_id = :committees_id;

UPDATE `candidate_office_records_contributions`
SET
    candidate_office_records_id = (
        SELECT id FROM `candidate_office_records` 
        WHERE fec_cand_id = :updated_fec_cand_id
    ),
    contributions_id = (
        SELECT id FROM `contributions` 
        WHERE sub_id = :updated_sub_id
    )
WHERE
    candidate_office_records_id = :candidate_office_records_id
    AND contributions_id = :contributions_id;

UPDATE `cycles_candidate_office_records`
SET
    cycles_year = :updated_cycles_year,
    candidate_office_records_id = (
        SELECT id FROM `candidate_office_records` 
        WHERE fec_cand_id = :updated_fec_cand_id
    )
WHERE
    cycles_year = :current_cycles_year
    AND candidate_office_records_id = :candidate_office_records_id;

UPDATE `cycles_contributions`
SET
    cycles_year = :updated_cycles_year,
    contributions_id = (
        SELECT id FROM `contributions` 
        WHERE sub_id = :updated_sub_id
    )
WHERE
    cycles_year = :current_cycles_year
    AND contributions_id = :contributions_id;

UPDATE `election_years_candidate_office_records`
SET
    election_years_year = :updated_election_years_year,
    candidate_office_records_id = (
        SELECT id FROM `candidate_office_records` 
        WHERE fec_cand_id = :updated_fec_cand_id
    )
WHERE
    election_years_year = :current_election_years_year
    AND candidate_office_records_id = :candidate_office_records_id;

UPDATE `election_years_contributions`
SET
    election_years_year = :updated_election_years_year,
    contributions_id = (
        SELECT id FROM `contributions` 
        WHERE sub_id = :updated_sub_id
    )
WHERE
    election_years_year = :current_election_years_year
    AND contributions_id = :contributions_id;

-- DELETE: This cascades all the M:M mappings but does not cascade the other "Mapped Table"
DELETE FROM `candidate_office_records`
WHERE name = :name_input_from_drop_down;