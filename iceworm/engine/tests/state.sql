drop table if exists things;
drop table if exists things_vers;

create table things(
  _seq serial,
  _at timestamp not null default current_timestamp,
  id varchar primary key not null,
  data text not null,
  _meta text not null
);

create table things_vers(
  _ver serial primary key,
  _seq integer not null,
  _at timestamp not null,
  id varchar not null,
  data text not null,
  _meta text not null
);

create index _things_seq_index on things (_seq);
create index _things_at_index on things (_at);

create index _things_vers_seq_index on things (_seq);
create index _things_vers_id_seq_index on things (id, _seq);
create index _things_vers_at_id_seq_index on things (_at, id, _seq);

create or replace function _things_before_write_function() returns trigger as $$ begin
  if new._seq != old._seq then
    raise exception 'cannot update _seq';
  end if;

  if new._at != old._at then
    raise exception 'cannot update _at';
  end if;

  if new.id != old.id then
    raise exception 'cannot update id';
  end if;

  new._at = now();

  return new;
end $$ language 'plpgsql';

create trigger _things_before_write_trigger before insert or update on things
for each row execute procedure _things_before_write_function();

create or replace function _things_after_write_function() returns trigger as $$ begin
  insert into things_vers (_seq, _at, id, data, _meta) values (new._seq, new._at, new.id, new.data, new._meta);

  return null;
end $$ language 'plpgsql';

create trigger _things_after_write_trigger after insert or update on things
for each row execute procedure _things_after_write_function();
