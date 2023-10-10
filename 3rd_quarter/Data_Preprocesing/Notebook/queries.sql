-- Active: 1696711558995@@localhost@3306@data_preprocessing
-- Instructions:
-- Give me all the bathroom information of people living in the neigbourhood of 'SawyerW'
SELECT 
    Id,
    BsmtFullBath,
    BsmtHalfBath,
    FullBath,
    HalfBath
FROM 
    data_preprocessing.data_imports
WHERE
    Neighborhood = 'SawyerW'