# encoding: UTF-8
# This file is auto-generated from the current state of the database. Instead
# of editing this file, please use the migrations feature of Active Record to
# incrementally modify your database, and then regenerate this schema definition.
#
# Note that this schema.rb definition is the authoritative source for your
# database schema. If you need to create the application database on another
# system, you should be using db:schema:load, not running all the migrations
# from scratch. The latter is a flawed and unsustainable approach (the more migrations
# you'll amass, the slower it'll run and the greater likelihood for issues).
#
# It's strongly recommended that you check this file into your version control system.

ActiveRecord::Schema.define(version: 20160315225039) do

  # These are extensions that must be enabled in order to support this database
  enable_extension "plpgsql"
  enable_extension "postgis"
  enable_extension "hstore"

  create_table "nodes", id: :bigserial, force: :cascade do |t|
    t.integer  "version",                                            null: false
    t.integer  "user_id",                                            null: false
    t.datetime "tstamp",                                             null: false
    t.integer  "changeset_id", limit: 8,                             null: false
    t.hstore   "tags"
    t.geometry "geom",         limit: {:srid=>4326, :type=>"point"}
  end

  add_index "nodes", ["geom"], name: "idx_nodes_geom", using: :gist

  create_table "relation_members", id: false, force: :cascade do |t|
    t.integer "relation_id", limit: 8, null: false
    t.integer "member_id",   limit: 8, null: false
    t.string  "member_type", limit: 1, null: false
    t.text    "member_role",           null: false
    t.integer "sequence_id",           null: false
  end

  add_index "relation_members", ["member_id", "member_type"], name: "idx_relation_members_member_id_and_type", using: :btree

  create_table "relations", id: :bigserial, force: :cascade do |t|
    t.integer  "version",                null: false
    t.integer  "user_id",                null: false
    t.datetime "tstamp",                 null: false
    t.integer  "changeset_id", limit: 8, null: false
    t.hstore   "tags"
  end

  create_table "schema_info", primary_key: "version", force: :cascade do |t|
  end

  create_table "users", force: :cascade do |t|
    t.text "name", null: false
  end

  create_table "way_nodes", id: false, force: :cascade do |t|
    t.integer "way_id",      limit: 8, null: false
    t.integer "node_id",     limit: 8, null: false
    t.integer "sequence_id",           null: false
  end

  add_index "way_nodes", ["node_id"], name: "idx_way_nodes_node_id", using: :btree

  create_table "ways", id: :bigserial, force: :cascade do |t|
    t.integer  "version",                                               null: false
    t.integer  "user_id",                                               null: false
    t.datetime "tstamp",                                                null: false
    t.integer  "changeset_id", limit: 8,                                null: false
    t.hstore   "tags"
    t.integer  "nodes",        limit: 8,                                             array: true
    t.geometry "linestring",   limit: {:srid=>4326, :type=>"geometry"}
    t.integer  "cost"
  end

  add_index "ways", ["linestring"], name: "idx_ways_linestring", using: :gist
  add_index "ways", ["nodes"], name: "nodes_idx", using: :gin

end
