class CreateSegments < ActiveRecord::Migration
  def change
    create_table :segments do |t|
      t.decimal :startlat, precision: 11, scale: 6
      t.decimal :startlong, precision: 11, scale: 6
      t.decimal :cost, precision: 11, scale: 6
      t.decimal :endlat, precision: 11, scale: 6
      t.decimal :endlong, precision: 11, scale: 6
    end
  end
end