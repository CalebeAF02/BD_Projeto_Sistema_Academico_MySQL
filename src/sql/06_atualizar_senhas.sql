-- =====================================================================
-- Migração: atualiza senhas placeholder para hashes reais (werkzeug scrypt)
-- Executar APÓS 05_seeds.sql.
-- Senha padrão de todas as contas de demonstração: senha123
-- Hashes gerados com werkzeug.security.generate_password_hash(method='scrypt')
-- =====================================================================

USE projeto_unb;

UPDATE conta SET senha = 'scrypt:32768:8:1$PMfvScVtSSVpSHhk$1b84bc0992e5bcaacad4b4bd18da6cb87ec5f1434e766e3450ddde5ba4ae2025eefa4f78badd2d734f575e9288596db2a0d30076f23276736c9716380a3d28b6' WHERE id = 1;
UPDATE conta SET senha = 'scrypt:32768:8:1$KPJOUvS4XALCN9Mf$0c01e9650eca1ab8753c20d31ccf8abe6667ea20e2240f4ce4eb95ca4798582b9be9cbfbfee71054efd2ea24b80954d1427685b5069395db12a1fa0ac1ce9852' WHERE id = 2;
UPDATE conta SET senha = 'scrypt:32768:8:1$GYTW5Oti4Xo5rYHX$cd488e629074092acb2615d64a3d867324b0a332e7c0bad9b7f74a89ccf6482c01d01ad70adc24d101e03b3c58f6e3db3d4e8ba193db77c45ab1ac7de1df65c8' WHERE id = 3;
UPDATE conta SET senha = 'scrypt:32768:8:1$krLlRCLeQgt2L2l0$c3faa2a9d0c964e7f8e85dd8922e53dcdb093e75fdc01019c60753649f41d4b741ac9407052be6ccc295a74c8caa574d21956cce512d8bf8caf807ae474ec17f' WHERE id = 4;
UPDATE conta SET senha = 'scrypt:32768:8:1$oE9bEVdQnZg8UJQP$d391571184f4c63763e81c04b32bf0252419dafd5caf16e581fdb54827dc90f124321ab0769a3c17be7907b4443db43cf03ff5ad1bd1dd49821ee55c1a0ba600' WHERE id = 5;
UPDATE conta SET senha = 'scrypt:32768:8:1$RuPlAlUg4uG8RSsA$71d2c11690e3aa1c13486274674c8ff89c25b6e3694efbaa930a75fd1340b206579dc2f34b5a1a33bb297c7805fa758aefd6c5dd9ef89d1979b7beba04c2551a' WHERE id = 6;
UPDATE conta SET senha = 'scrypt:32768:8:1$GZktto6pU3arhjwJ$939c93536f92b8ad7c28259e81eda1361bc587718cbf1361e23b3645ec2eb39e73d88644293bd8a86cba47314fabda0dc5a0bafab3681119ea66add97d87922e' WHERE id = 7;
UPDATE conta SET senha = 'scrypt:32768:8:1$EwwLvmz9l0ogcLYt$1dd079d9d6dfb598930a6085b07965db043026a9f2beee636e9d2bf449b68238f72f10335d9f7fceb022e754cec06a5638812b578a711c3c046c2577f2334279' WHERE id = 8;
UPDATE conta SET senha = 'scrypt:32768:8:1$Dp5FTr9XoFCOrYTG$749ebc538943b6bc40852738787d8332350e00ec75ba9882680b87d21a2656af04d08a6609f4648831db75236f01a4db40a291d3a9a79a207f29bbc0fb5b373d' WHERE id = 9;
UPDATE conta SET senha = 'scrypt:32768:8:1$nBa3OHTpoG2w7aho$bae58d57d907d1d4ad63567634d9e5625ba0087139a0ad11c9d10097cb7d7e9477be7560b895d9f277511d4b8e81a43d0764ff0e8bac8365d448dc927b5363c6' WHERE id = 10;
