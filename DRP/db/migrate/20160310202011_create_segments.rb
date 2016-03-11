class CreateSegments < ActiveRecord::Migration
  def change
    create_table :segments do |t|
      t.decimal :startlat
      t.decimal :startlong
      t.decimal :cost
      t.decimal :endlat
      t.decimal :endlong
    end
  end
end
