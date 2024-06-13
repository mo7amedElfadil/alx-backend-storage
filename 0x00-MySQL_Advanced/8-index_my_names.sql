-- create index idx_name_first on names with the first letter of the name

-- create the index
CREATE INDEX idx_name_first ON names (name(1));
