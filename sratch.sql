INSERT INTO `cs340_umj`.`office_types` (code, name)
VALUES
	('P', 'President'),
    ('H', 'House of Representatives'),
    ('S', 'Senate');
    

INSERT INTO `cs340_umj`.`contributor_types` (code, name)
VALUES
    ('CAN', 'DummyData1'),
    ('CCM', 'DummyData2'),
    ('COM', 'DummyData3'),
    ('IND', 'DummyData4'),
    ('ORG', 'DummyData5'),
    ('PAC', 'DummyData6'),
    ('PTY', 'DummyData7');

INSERT INTO `cs340_umj`.`report_types` (code, name)
VALUES
    ('12C', 'a1'),
    ('12G', 'a2'),
    ('12P', 'a3'),
    ('12R', 'a4'),
    ('12S', 'a5'),
    ('30D', 'a6'),
    ('30G', 'a7'),
    ('30P', 'a8'),
    ('30R', 'a9'),
    ('30S', 'a10'),
    ('60D', 'a11'),
    ('ADJ', 'a12'),
    ('CA', 'a13'),
    ('M10', 'a14'),
    ('M11', 'a15'),
    ('M12', 'a16'),
    ('M2', 'a17'),
    ('M3', 'a18'),
    ('M4', 'a19'),
    ('M5', 'a20'),
    ('M6', 'a21'),
    ('M7', 'a22'),
    ('M8', 'a22oopsiewasduplicate'),
    ('M9', 'a23'),
    ('MY', 'a24'),
    ('Q1', 'a25'),
    ('Q2', 'a26'),
    ('Q3', 'a27'),
    ('TER', 'a28'),
    ('YE', 'a29'),
    ('90S', 'a30'),
    ('90D', 'a31'),
    ('48H', 'a32'),
    ('24H', 'a33');
    
INSERT INTO `cs340_umj`.`party_types` (code, short_name)
VALUES
    ('1', 'DEM'),
    ('2', 'REP'),
    ('3', 'IND');
    

INSERT INTO `cs340_umj`.`incumbent_challenger_statuses` (code, name)
VALUES
    ('I', 'Incumbent'),
    ('C', 'Challenger'),
    ('O', 'Open Seat');

INSERT INTO `cs340_umj`.`amendment_indicators` (code, name)
VALUES
    ('N', 'New report'),
    ('A', 'Amendment to previous report'),
    ('T', 'Termination report');


INSERT INTO `cs340_umj`.`election_years` (year)
VALUES
    ('2018'),
    ('2019'),
    ('2020'),
    ('2021'),
    ('2022'),
    ('2023'),
    ('2024'),
    ('2025'),
    ('2026');



INSERT INTO `cs340_umj`.`transaction_types` (code, name)
VALUES
    ('10', 'a1'),
    ('10J', 'a2'),
    ('11', 'a3'),
    ('11J', 'a4'),
    ('12', 'a5'),
    ('13', 'a6'),
    ('15', 'a7'),
    ('15C', 'a8'),
    ('15E', 'a9'),
    ('15F', 'a10'),
    ('15I', 'a11'),
    ('15J', 'a12'),
    ('15T', 'a13'),
    ('15Z', 'a14'),
    ('16C', 'a15'),
    ('16F', 'a16'),
    ('16G', 'a17'),
    ('16H', 'a18'),
    ('16J', 'a19'),
    ('16K', 'a20'),
    ('16L', 'a21'),
    ('16R', 'a22'),
    ('16U', 'a23'),
    ('17R', 'a24'),
    ('17U', 'a25'),
    ('17Y', 'a26'),
    ('17Z', 'a27'),
    ('18G', 'a28'),
    ('18H', 'a29'),
    ('18J', 'a30'),
    ('18K', 'a31'),
    ('18L', 'a32'),
    ('18U', 'a33'),
    ('19', 'a34'),
    ('19J', 'a35'),
    ('20', 'a36'),
    ('20A', 'a37'),
    ('20B', 'a38'),
    ('20C', 'a39'),
    ('20D', 'a40'),
    ('20F', 'a41'),
    ('20G', 'a42'),
    ('20R', 'a43'),
    ('20V', 'a44'),
    ('20Y', 'a45'),
    ('', 'a46'),
    ('21Y', 'a47'),
    ('22G', 'a48'),
    ('22H', 'a49'),
    ('22J', 'a50'),
    ('22K', 'a51'),
    ('22L', 'a52'),
    ('22R', 'a53'),
    ('22U', 'a54'),
    ('22X', 'a55'),
    ('22Y', 'a56'),
    ('22Z', 'a57'),
    ('23Y', 'a58'),
    ('24A', 'a59'),
    ('24C', 'a60'),
    ('24E', 'a61'),
    ('24F', 'a62'),
    ('24G', 'a63'),
    ('24H', 'a64'),
    ('24I', 'a65'),
    ('24K', 'a66'),
    ('24N', 'a67'),
    ('24P', 'a68'),
    ('24R', 'a69'),
    ('24T', 'a70'),
    ('24U', 'a71'),
    ('24Z', 'a72'),
    ('28L', 'a73'),
    ('29', 'a74'),
    ('30', 'a75'),
    ('30T', 'a76'),
    ('30K', 'a77'),
    ('30G', 'a78'),
    ('30J', 'a79'),
    ('30F', 'a80'),
    ('31', 'a81'),
    ('31T', 'a82'),
    ('31K', 'a83'),
    ('31G', 'a84'),
    ('31J', 'a85'),
    ('31F', 'a86'),
    ('32', 'a87'),
    ('32T', 'a88'),
    ('32K', 'a89'),
    ('32G', 'a90'),
    ('32J', 'a91'),
    ('32F', 'a92'),
    ('40', 'a93'),
    ('40Y', 'a94'),
    ('40T', 'a95'),
    ('40Z', 'a96'),
    ('41', 'a97'),
    ('41Y', 'a98'),
    ('41T', 'a99'),
    ('41Z', 'a100'),
    ('42', 'a101'),
    ('42Y', 'a102'),
    ('42T', 'a103'),
    ('42Z', 'a104');

INSERT INTO `cs340_umj`.`candidates` (first_name, last_name, middle_name, email)
VALUES 
    ('barack', 'obama', 'hussein', 'barack.h.obama@example.com'),
    ('donald', 'john', 'trump', 'donald.j.trump@example.com'),
    ('joseph', 'robinette', 'biden', 'joseph.r.biden@example.com');

-- Above line is successful

/*
real data used to demonstrate some complexity and future friction points.

note: each real person candidate will often have more than one of these records
even in the same file. this is how the data is designed. note the inconsistencies
in the name field with President Biden.
top record is for runnin for reelection and second record is for being in office?
we dont have to solve this but we need to understand that this will happen often.

our manual mapping of candidates to these candidate_office_records is the secret
to the whole project.

how you say?

1. make candidate record
2. Use first, middle, last in an ilike query (with other filters so we dont try to scan millions of records),
present that data to the user for manual mapping.
3. prob need to add some special indices like ngrams for special searches.

source: candidate master 2023-2024

begin ---
P40011678|BIDEN, JOSEPH JR|DEM|2024|US|P|00|C|N||1120 20TH STREET NW|SUITE 250|WASHINGTON|DC|20036
P40011686|BIDEN, JOSEPH R MR JR|DEM|2024|US|P|00|C|N||1120 20TH STREET NW|SUITE 250|WASHINGTON|DC|20036

S4CA00464|MANDELA, BARACK OBAMA MR.|REP|2024|CA|S|00|O|N||7348 MILTON AVENUE|APT. 1|WHITTIER|CA|90602
P40005985|HAUSKINS, DANIEL OBAMA MR JR|GWP|2024|US|P|00|C|N||1234 21ST ST.||ROCK ISLAND|IL|61201

S2AK00176|STEPHENS, JOE TRUMP AKA NOT MURKOWSKI|AKI|2022|AK|S|00|C|N|C00787093|3609 TONGASS AVENUE|5416|KETCHIKAN|AK|99901
P80001571|TRUMP, DONALD J.|REP|2024|US|P|00|C|C|C00828541|P.O. BOX 13570||ARLINGTON|VA|22219
end ---


source: candidate all 2023-2024
NOTE: notice that date metadata seems like a last updated sort of deal
NOTE: this file looks cleaner and might have less dupes? we still need data in the other file
for election year but we could process this file first and then use the other file above
to map the candidate
begin---
P80000722|BIDEN, JOSEPH R JR|I|1|DEM|360.3|0|423440.56|2800|1787497.02|1364416.76|0|0|0|0|0|0|0|00|00||||||0|0|03/31/2023|0|0

no result for "obama"

P80001571|TRUMP, DONALD J.|C|2|REP|14449602.19|14053900.4|3538555.97|0|3020902.11|13931948.33|0|0|0|0|0|255109.66|10840.8|00|00||||||0|0|03/31/2023|0|0

end---


NOTE: we are missing TTL_DISB, TRANS_TO_AUTH, OTHER_POL_CMTE_CONTRIB from All candidates file this is prob okay
since we didnt but it in schema but it would be cool to have.
NOTE: all of the above blows the scope for the class project but it is good for any future
the project could have.
NOTE: We probably should add category tables for cand_office_st and cand_office_district
but maybe that is overly normalized... hmmmm
*/

INSERT INTO `cs340_umj`.`candidate_office_records` (
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
) VALUES
    (
        'P80000722', -- fec_cand_id
        'BIDEN, JOSEPH R JR', -- name
        360.3, -- ttl_receipts 
        0, -- trans_from_auth
        1787497.02, -- coh_bop
        1364416.76, -- coh_cop
        0, -- cand_contrib
        0, -- cand_loans
        0, -- other_loans
        0, -- cand_loan_repay
        0, -- other_loan_repay
        0, -- debts_owed_by
        0, -- ttl_indiv_contrib
        '00', -- cand_office_st,
        '00', -- cand_office_district,
        0, -- pol_pty_contrib
        '2023-03-31', -- cvg_end_dt
        0, -- indiv_refund
        0, -- cmte_refund
        (SELECT id FROM `cs340_umj`.`office_types` WHERE code = 'P'),
        NULL,
        (SELECT id FROM `cs340_umj`.`party_types` WHERE short_name = 'DEM'),
        (SELECT id FROM `cs340_umj`.`incumbent_challenger_statuses` WHERE code = 'I')
    ),
    (
        'P80001571', -- fec_cand_id
        'TRUMP, DONALD J.', -- name
        14449602.19, -- ttl_receipts 
        14053900.4, -- trans_from_auth
        3020902.11, -- coh_bop
        13931948.33, -- coh_cop
        0, -- cand_contrib
        0, -- cand_loans
        0, -- other_loans
        0, -- cand_loan_repay
        0, -- other_loan_repay
        255109.66, -- debts_owed_by
        10840.8, -- ttl_indiv_contrib
        '00', -- cand_office_st,
        '00', -- cand_office_district,
        0, -- pol_pty_contrib
        '2023-03-31', -- cvg_end_dt
        0, -- indiv_refund
        0, -- cmte_refund
        (SELECT id FROM `cs340_umj`.`office_types` WHERE code = 'P'),
        NULL,
        (SELECT id FROM `cs340_umj`.`party_types` WHERE short_name = 'REP'),
        (SELECT id FROM `cs340_umj`.`incumbent_challenger_statuses` WHERE code = 'C')
    );


INSERT INTO `cs340_umj`.`committee_types` (code, name, explanation)
VALUES
    ('C', 'C', 'really long explanation or maybe it is short just depends. cna also be null'),
    ('D', 'D', 'long explanation'),
    ('E', 'E', 'long explanation'),
    ('H', 'H', 'long explanation'),
    ('I', 'I', 'long explanation'),
    ('N', 'N', 'long explanation'),
    ('O', 'O', 'long explanation'),
    ('P', 'P', 'long explanation'),
    ('Q', 'Q', 'long explanation'),
    ('S', 'S', 'long explanation'),
    ('U', 'U', 'long explanation'),
    ('V', 'V', 'long explanation'),
    ('W', 'W', 'long explanation'),
    ('X', 'X', 'long explanation'),
    ('Y', 'Y', 'long explanation'),
    ('Z', 'Z', 'long explanation');



/*
NOTE: for the record I did contributions first and then circled back to do
committees up here.
It seems like our change to make committees optional was the right one.
many committee ids exist in the master file and they arent all in pas224 but they might
be in the other contributions file maybe.
source: Committe master file. record: cm24
-- begin
C00748582|REALLY AMERICAN PAC|SKIP|SKIP||
WASHINGTON|DC|20015|U|O||M||NONE|

C00489799|PLANNED PARENTHOOD VOTES|LOUIE, MAGGIE|123 WILLIAM ST.||NEW YORK|NY|10038|U|O||M||NONE|

-- end

TODO: Remove employer because it is not in the master file.
TODO: contributor_types shoudl not have landed in this table this should be committe_type and we also need
a new table with that.
TODO: contributor type should only go on contribution
*/
INSERT INTO `cs340_umj`.`committees` (
    cmte_id,
    name,
    city,
    state,
    zip_code,
    committee_types_id
) VALUES
    (
        'C00748582',
        'REALLY AMERICAN PAC',
        'WASHINGTON',
        'DC',
        '20015', -- zip_code
        (SELECT id FROM `cs340_umj`.`committee_types` WHERE code = 'O')
    ),
    (
        'C00489799',
        'PLANNED PARENTHOOD VOTES',
        'NEW YORK',
        'NY',
        '10038', -- zip_code
        (SELECT id FROM `cs340_umj`.`committee_types` WHERE code = 'O')
    );




/*
source: contributions from committees data 2024 aka pas224
search conducted on both fec candidate ids above
I replaced all the goofy | characters with , so I could easily import it as a csv for viz too.

THIS DATA ID C00748582 IS ABOVE with what looks to be one name and below with another.

THIS IS REAL FEC DATA AND THE SOURCE SEEMS LIKE
IT SAYS IT SHOULD!!!!

THIS IS LIKELY my misunderstand of their confusing data.....?

-- begin
TRUMP ---
C00748582|N|M2|P2024|202302209578707392|24A|ORG|BLUE WAVE COMMUNICATIONS LLC|CHICAGO|IL|60602|||01092023|7000|P80001571|P80001571|SE.28013|1690370|||4022120231732517006
C00748582|N|M2|P2024|202302209578707392|24A|ORG|BLUE WAVE COMMUNICATIONS LLC|CHICAGO|IL|60602|||01232023|7000|P80001571|P80001571|SE.28014|1690370|||4022120231732517007

C00489799|A|M3|P2024|202304189581037688|24A|PAC|PLANNED PARENTHOOD ACTION FUND, INC.|NEW YORK|NY|100383804|||02142023|200|P80001571|P80001571|500098872|1700821|||4042020231743494020
TRUMP ---

-- end

It is unclear whether paying to take out an ad against a candidate is captured in the above records.
I think I recall reading something about that being in some data but that is a future interest
that does not change the data we parse.



*/

INSERT INTO `cs340_umj`.`contributions` (
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
) VALUES (
    'P2024', -- transaction_pgi,
    '202302209578707392', -- image_num,
    '2023-01-09', -- transaction_dt,
    7000, -- transaction_amt,
    'SE.28013', -- trans_id,
    1690370, -- file_num,
    NULL, -- memo_cd,
    NULL, -- memo_text,
    4022120231732517006, -- sub_id,
    (SELECT id FROM `cs340_umj`.`committees` WHERE cmte_id = 'C00748582'),
    (SELECT id FROM `cs340_umj`.`report_types` WHERE code = 'M2'),
    (SELECT id FROM `cs340_umj`.`transaction_types` WHERE code = '24A'),
    (SELECT id FROM `cs340_umj`.`amendment_indicators` WHERE code = 'N'),
    (SELECT id FROM `cs340_umj`.`contributor_types` WHERE code = 'ORG')
);

-- TODO: mORE ^^^



-- EVEN YEARS ONLY FOR CYCLES
INSERT INTO `cs340_umj`.`cycles` (year)
VALUES
    ('2018'),
    ('2020'),
    ('2022'),
    ('2024');